def test_file_task_handler_rotate_size_limit(self):
    def reset_log_config(update_conf):
        import logging.config

        logging_config = DEFAULT_LOGGING_CONFIG
        logging_config = deep_update(logging_config, update_conf)
        logging.config.dictConfig(logging_config)

    def task_callable(ti):
        pass

    max_bytes_size = 60000
    update_conf = {"handlers": {"task": {"max_bytes": max_bytes_size, "backup_count": 1}}}
    reset_log_config(update_conf)
    dag = DAG("dag_for_testing_file_task_handler_rotate_size_limit", start_date=DEFAULT_DATE)
    task = PythonOperator(
        task_id="task_for_testing_file_log_handler_rotate_size_limit",
        python_callable=task_callable,
        dag=dag,
    )
    triggered_by_kwargs = {"triggered_by": DagRunTriggeredByType.TEST} if AIRFLOW_V_3_0_PLUS else {}
    dagrun = dag.create_dagrun(
        run_type=DagRunType.MANUAL,
        state=State.RUNNING,
        logical_date=DEFAULT_DATE,
        data_interval=dag.timetable.infer_manual_data_interval(run_after=DEFAULT_DATE),
        **triggered_by_kwargs,
    )
    ti = TaskInstance(task=task, run_id=dagrun.run_id)

    ti.try_number = 1
    ti.state = State.RUNNING

    logger = ti.log
    ti.log.disabled = False

    file_handler = next(
        (handler for handler in logger.handlers if handler.name == FILE_TASK_HANDLER), None
    )
    assert file_handler is not None

    set_context(logger, ti)
    assert file_handler.handler is not None
    # We expect set_context generates a file locally, this is the first log file
    # in this test, it should generate 2 when it finishes.
    log_filename = file_handler.handler.baseFilename
    assert os.path.isfile(log_filename)
    assert log_filename.endswith("1.log"), log_filename

    # mock to generate 2000 lines of log, the total size is larger than max_bytes_size
    for i in range(1, 2000):
        logger.info("this is a Test. %s", i)

    # this is the rotate log file
    log_rotate_1_name = log_filename + ".1"
    assert os.path.isfile(log_rotate_1_name)

    current_file_size = os.path.getsize(log_filename)
    rotate_file_1_size = os.path.getsize(log_rotate_1_name)
    assert rotate_file_1_size > max_bytes_size * 0.9
    assert rotate_file_1_size < max_bytes_size
    assert current_file_size < max_bytes_size

    # Return value of read must be a tuple of list and list.
    logs, metadatas = file_handler.read(ti)

    # the log content should have the filename of both current log file and rotate log file.
    find_current_log = False
    find_rotate_log_1 = False
    for log in logs:
        if log_filename in str(log):
            find_current_log = True
        if log_rotate_1_name in str(log):
            find_rotate_log_1 = True
    assert find_current_log is True
    assert find_rotate_log_1 is True

    assert isinstance(logs, list)
    # Logs for running tasks should show up too.
    assert isinstance(logs, list)
    assert isinstance(metadatas, list)
    assert len(logs) == len(metadatas)
    assert isinstance(metadatas[0], dict)

    # Remove the two generated tmp log files.
    os.remove(log_filename)
    os.remove(log_rotate_1_name)