def test_file_task_handler_running(self):
    def task_callable(ti):
        ti.log.info("test")

    dag = DAG("dag_for_testing_file_task_handler", schedule=None, start_date=DEFAULT_DATE)
    task = PythonOperator(
        task_id="task_for_testing_file_log_handler",
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

    ti.try_number = 2
    ti.state = State.RUNNING

    logger = ti.log
    ti.log.disabled = False

    file_handler = next(
        (handler for handler in logger.handlers if handler.name == FILE_TASK_HANDLER), None
    )
    assert file_handler is not None

    set_context(logger, ti)
    assert file_handler.handler is not None
    # We expect set_context generates a file locally.
    log_filename = file_handler.handler.baseFilename
    assert os.path.isfile(log_filename)
    assert log_filename.endswith("2.log"), log_filename

    logger.info("Test")

    # Return value of read must be a tuple of list and list.
    logs, metadatas = file_handler.read(ti)
    assert isinstance(logs, list)
    # Logs for running tasks should show up too.
    assert isinstance(logs, list)
    assert isinstance(metadatas, list)
    assert len(logs) == 2
    assert len(logs) == len(metadatas)
    assert isinstance(metadatas[0], dict)

    # Remove the generated tmp log file.
    os.remove(log_filename)