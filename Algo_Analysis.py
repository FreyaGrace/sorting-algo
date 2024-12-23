import numpy as np
import matplotlib.pyplot as plt
import time



def visualize(data, title, pause_time=0.1, max_frames=50):
    # Initialize frame counter
    visualize.counter = 0
    """Visualize the sorting process with a frame limit."""
    if visualize.counter >= max_frames:  # Stop if frame limit is reached
        print("Reached frame limit. Stopping visualization...")
        raise StopIteration  # Gracefully stop the sorting

    plt.clf()
    plt.bar(range(len(data)), data, color='blue')
    plt.title(f"{title} (Frame {visualize.counter + 1}/{max_frames})")
    plt.xlabel('Index')
    plt.ylabel('Value')
    plt.ylim(0, max(data) + 10)
    plt.pause(pause_time)

    visualize.counter += 1  # Increment frame counter

# Heap Sort
def heapify(arr, n, i, max_frames):
    largest = i
    left = 2 * i + 1
    right = 2 * i + 2

    if left < n and arr[left] > arr[largest]:
        largest = left

    if right < n and arr[right] > arr[largest]:
        largest = right

    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        visualize(arr, "Heap Sort - Swapping {} and {}".format(arr[i], arr[largest]), max_frames=max_frames)
        heapify(arr, n, largest, max_frames)

def heap_sort(arr, max_frames):
    n = len(arr)
    # Build heap
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i, max_frames)
    # One by one extract elements from heap
    for i in range(n - 1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]
        visualize(arr, "Heap Sort - Extracting {}".format(arr[i]), max_frames=max_frames)
        heapify(arr, i, 0, max_frames)

# Quick Sort
def quick_sort(arr, low, high, max_frames):
    if low < high:
        pi = partition(arr, low, high, max_frames)
        quick_sort(arr, low, pi - 1, max_frames)
        quick_sort(arr, pi + 1, high, max_frames)

def partition(arr, low, high, max_frames):
    pivot = arr[high]
    i = low - 1
    for j in range(low, high):
        if arr[j] < pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
            visualize(arr, "Quick Sort", max_frames=max_frames)  # Visualize during partitioning
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    visualize(arr, "Quick Sort", max_frames=max_frames)  # Visualize after partitioning
    return i + 1

# Merge Sort
def merge_sort(arr, max_frames):
    if len(arr) > 1:
        mid = len(arr) // 2
        L = arr[:mid]
        R = arr[mid:]

        merge_sort(L, max_frames)
        merge_sort(R, max_frames)

        i = j = k = 0

        while i < len(L) and j < len(R):
            if L[i] < R[j]:
                arr[k] = L[i]
                i += 1
            else:
                arr[k] = R[j]
                j += 1
            k += 1
            visualize(arr, "Merge Sort", max_frames=max_frames)  # Visualize during merging

        while i < len(L):
            arr[k] = L[i]
            i += 1
            k += 1
            visualize(arr, "Merge Sort", max_frames=max_frames)  # Visualize after adding remaining elements

        while j < len(R):
            arr[k] = R[j]
            j += 1
            k += 1
            visualize(arr, "Merge Sort", max_frames=max_frames)  # Visualize after adding remaining elements

# Benchmarking function
def benchmark_sorting_algorithm(sort_func, data):
    start_time = time.time()
    sort_func(data)  # Run sorting without visualization for benchmarking
    return time.time() - start_time

def benchmark(size, max_frames):
    data = np.random.randint(1, 10000, size).tolist()  # Generate data based on user input
    results = {}

    # Benchmark Heap Sort without visualization
    heap_time = benchmark_sorting_algorithm(lambda arr: heap_sort(arr.copy(), max_frames), data)
    results['Heap Sort'] = heap_time

    # Benchmark Quick Sort without visualization
    quick_time = benchmark_sorting_algorithm(lambda arr: quick_sort(arr.copy(), 0, len(arr) - 1, max_frames), data)
    results['Quick Sort'] = quick_time

    # Benchmark Merge Sort without visualization
    merge_time = benchmark_sorting_algorithm(lambda arr: merge_sort(arr.copy(), max_frames), data)
    results['Merge Sort'] = merge_time

    # Performance Analytics
    print("\nBenchmark Results:")
    print(f"Dataset Size: {size}")
    for sort_type, time_taken in results.items():
        print(f"{sort_type}: {time_taken:.6f} seconds")
    
    total_time = sum(results.values())
    print(f"Total Time Taken: {total_time:.6f} seconds")

# Main function with options menu
def main():
    plt.ion()  # Enable interactive mode for real-time plotting

    while True:
        print("\nOptions:")
        print("1. Visualize Sorting Algorithms")
        print("2. Benchmark Sorting Algorithms")
        print("3. Exit")

        choice = input("Choose an option (1-3): ").strip()

        if choice == '1':
            try:
                size = int(input("Enter the dataset size for visualization: "))
                max_frames = int(input("Enter the maximum number of frames to plot: "))

                data = np.random.randint(1, 100, size).tolist()
                visualize.counter = 0  # Reset frame counter

                print("\nChoose sorting algorithm to visualize:")
                print("1. Heap Sort")
                print("2. Quick Sort")
                print("3. Merge Sort")
                algo_choice = input("Choose an algorithm (1-3): ").strip()

                plt.figure(figsize=(10, 6))

                try:
                    start_time = time.time()  # Start timing visualization
                    if algo_choice == '1':
                        heap_sort(data, max_frames)
                    elif algo_choice == '2':
                        quick_sort(data, 0, len(data) - 1, max_frames)
                    elif algo_choice == '3':
                        merge_sort(data, max_frames)
                    else:
                        print("Invalid algorithm choice. Please try again.")
                    
                except StopIteration:
                    print("Visualization stopped early due to frame limit.")

            except ValueError as e:
                print(f"Invalid input: {e}")

        elif choice == '2':
            try:
                size = int(input("Enter the dataset size for benchmarking: "))
                max_frames = int(input("Enter the maximum number of frames to plot: "))
                start_time = time.time()  # Start timing benchmarking
                benchmark(size,max_frames)  # Run benchmarking with the specified size
                end_time = time.time()  # End timing benchmarking
                print(f"Total benchmarking time: {end_time - start_time:.6f} seconds")
            except ValueError as e:
                print(f"Invalid input: {e}")

        elif choice == '3':
            print("Exiting the program. Goodbye!")
            end_time = time.time()  # End timing visualization
            print(f"Total visualization time: {end_time - start_time:.6f} seconds")
                    
            # Display performance analytics for visualization
            print(f"\nPerformance Analytics for {['Heap Sort', 'Quick Sort', 'Merge Sort'][int(algo_choice)-1]}:")
            print(f"Dataset Size: {size}, Frames: {visualize.counter}, Visualization Time: {end_time - start_time:.6f} seconds")
            break
            

        else:
            print("Invalid choice, please try again.")

# Run the program
if __name__ == "__main__":
    main()
