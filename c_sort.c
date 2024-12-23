#include <stdio.h>
#include <stdlib.h>
#include <time.h>

// Declare the sorting functions as extern
extern void heap_sort(int *arr, int low, int high, int max_frames, int *frame_counter);
extern void quick_sort(int *arr, int low, int high, int max_frames, int *frame_counter);
extern void merge_sort(int *arr, int left, int right, int max_frames, int *frame_counter);
extern double benchmark_sorting_algorithm_no_vis(void (*sort_func)(int *, int, int, int, int *), int *data, int n, int max_frames);
// Visualization function (prints the array)
void visualize(int *arr, int size, const char *title, int max_frames, int *frame_counter) {
    if (*frame_counter >= max_frames) {
        printf("Maximum frames reached. Stopping visualization.\n");
        return;
    }
    printf("%s: ", title);
    for (int i = 0; i < size; i++) {
        printf("%d ", arr[i]);
    }
    printf("\n");
    (*frame_counter)++;
}

// Benchmark sorting algorithm without visualization
double benchmark_sorting_algorithm_no_vis(void (*sort_func)(int *, int, int, int, int *), int *data, int n, int max_frames) {
    clock_t start_time = clock();
    sort_func(data, 0, n - 1, max_frames, (int *)malloc(sizeof(int)));  // Run sorting without visualization
    clock_t end_time = clock();
    return (double)(end_time - start_time) / CLOCKS_PER_SEC;
}

// Benchmarking function
void benchmark(int size, int max_frames) {
    int *data = (int *)malloc(size * sizeof(int));
    for (int i = 0; i < size; i++) {
        data[i] = rand() % 10000;
    }

    printf("\nBenchmarking Heap Sort\n");
    double heap_time = benchmark_sorting_algorithm_no_vis(heap_sort, data, size, max_frames);

    printf("\nBenchmarking Quick Sort\n");
    double quick_time = benchmark_sorting_algorithm_no_vis(quick_sort, data, size, max_frames);

    printf("\nBenchmarking Merge Sort\n");
    double merge_time = benchmark_sorting_algorithm_no_vis(merge_sort, data, size, max_frames);

    printf("\nBenchmark Results:\n");
    printf("Dataset Size: %d\n", size);
    printf("Heap Sort: %.6f seconds\n", heap_time);
    printf("Quick Sort: %.6f seconds\n", quick_time);
    printf("Merge Sort: %.6f seconds\n", merge_time);

    double total_time = heap_time + quick_time + merge_time;
    printf("Total Time Taken: %.6f seconds\n", total_time);

    free(data);
}

int main() {
    srand(time(NULL));  // Seed for random number generation

    while (1) {
        printf("\nOptions:\n");
        printf("1. Visualize Sorting Algorithms\n");
        printf("2. Benchmark Sorting Algorithms\n");
        printf("3. Exit\n");

        int choice;
        printf("Choose an option (1-3): ");
        scanf("%d", &choice);

        if (choice == 1) {
            int size, max_frames;
            printf("Enter the dataset size for visualization: ");
            scanf("%d", &size);
            printf("Enter the maximum number of frames to visualize: ");
            scanf("%d", &max_frames);

            int *data = (int *)malloc(size * sizeof(int));
            for (int i = 0; i < size; i++) {
                data[i] = rand() % 100;
            }

            printf("\nChoose sorting algorithm to visualize:\n");
            printf("1. Heap Sort\n");
            printf("2. Quick Sort\n");
            printf("3. Merge Sort\n");
            int algo_choice;
            printf("Choose an algorithm (1-3): ");
            scanf("%d", &algo_choice);

            int frame_counter = 0;
            if (algo_choice == 1) {
                heap_sort(data, 0, size - 1, max_frames, &frame_counter);
            } else if (algo_choice == 2) {
                quick_sort(data, 0, size - 1, max_frames, &frame_counter);
            } else if (algo_choice == 3) {
                merge_sort(data, 0, size - 1, max_frames, &frame_counter);
            } else {
                printf("Invalid algorithm choice.\n");
            }

            free(data);
        } else if (choice == 2) {
            int size, max_frames;
            printf("Enter the dataset size for benchmarking: ");
            scanf("%d", &size);
            printf("Enter the maximum number of frames for benchmarking: ");
            scanf("%d", &max_frames);

            benchmark(size, max_frames);
        } else if (choice == 3) {
            break;
        } else {
            printf("Invalid choice. Please choose between 1-3.\n");
        }
    }

    return 0;
}