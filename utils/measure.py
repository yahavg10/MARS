import time


def simulate_events(handler, num_events: int, folder_to_monitor: str):
    with handler.processor.strategy_pool.pool as executor:
        for i in range(num_events):
            for pair_part in "ab":
                src_path = f"{folder_to_monitor}/file{i}_{pair_part}.txt"
                executor.submit(handler.run_process, kwargs={'event_type': "created", 'src_path': src_path})

        executor.shutdown(wait=True)


def measure_execution_time(handler, num_events: int, folder_to_monitor: str):
    start_time = time.time()

    simulate_events(handler, num_events, folder_to_monitor)  # Simulate file creation events

    end_time = time.time()

    return end_time - start_time