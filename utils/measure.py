import time


def simulate_events(orchestrator, num_events: int, folder_to_monitor: str):
    with orchestrator.pipeline_executor.strategy_pool.pool as executor:
        for i in range(num_events):
            for pair_part in "ab":
                src_path = f"{folder_to_monitor}/file{i}_{pair_part}.txt"
                executor.submit(orchestrator.run_process, kwargs={'event_type': "created", 'src_path': src_path})

        executor.shutdown(wait=True)


def measure_execution_time(orchestrator, num_events: int, folder_to_monitor: str):
    start_time = time.time()

    simulate_events(orchestrator, num_events, folder_to_monitor)  # Simulate file creation events

    end_time = time.time()

    return end_time - start_time
