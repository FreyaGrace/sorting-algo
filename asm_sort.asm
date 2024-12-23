.386
.model flat, stdcall
option casemap:none

include \masm32\include\kernel32.inc
include \masm32\include\masm32.inc
includelib \masm32\lib\kernel32.lib
includelib \masm32\lib\masm32.lib

.data
    arr dd 9, 3, 5, 7, 2, 8, 1, 6, 4, 0   ; Array to be sorted
    arr_len dd 10                         ; Array length
    msgHeap db "Heap Sort Visualization:", 13, 10, 0
    msgDone db "Sorting Complete!", 13, 10, 0
    msgTime db "Time taken (ms): ", 0
    temp_buffer db 20 dup(?)              ; Buffer for integer to string conversion
    elapsedTime dd ?
    space db " ", 0


.code
start:
    ; Print initial message
    invoke StdOut, addr msgHeap

    ; Start timing
    invoke GetTickCount
    mov ebx, eax  ; Store start time

    ; Perform Heap Sort
    lea esi, arr
    mov ecx, 10  ; Array length
    call heap_sort

    ; Stop timing
    invoke GetTickCount
    sub eax, ebx  ; Calculate elapsed time
    mov elapsedTime, eax

    ; Print sorted array
    lea esi, arr
    mov ecx, 10
    call print_array

    ; Convert elapsed time to string and print
    mov eax, elapsedTime
    lea edi, temp_buffer
    call int_to_string
    invoke StdOut, addr msgTime
    invoke StdOut, addr temp_buffer
    invoke StdOut, addr msgDone


    ; Exit program
    invoke ExitProcess, 0

; Heap Sort Procedure
heap_sort proc
    push ecx
    mov ecx, 10
    shr ecx, 1  ; Start from the last non-leaf node
build_heap:
    push ecx
    lea esi, arr
    call heapify
    pop ecx
    dec ecx
    jnz build_heap
    pop ecx

    ; Extract elements
    push ecx
    mov ecx, 10
heap_extract:
    dec ecx
    lea esi, arr
    ; Swap root and last element
    mov eax, [esi]
    mov ebx, [esi + ecx * 4]
    mov [esi], ebx
    mov [esi + ecx * 4], eax

    ; Re-heapify
    push ecx
    call heapify
    pop ecx
    test ecx, ecx
    jnz heap_extract
    pop ecx
    ret
heap_sort endp

heapify proc
    push eax ebx ecx edx edi
    mov edi, 0  ; Current node index

heapify_loop:
    mov eax, edi
    shl eax, 1
    inc eax     ; Left child index
    cmp eax, ecx
    jge heapify_done  ; No left child

    mov ebx, [esi + eax * 4]  ; Left child
    inc eax                   ; Right child index
    cmp eax, ecx
    jge no_right_child

    mov edx, [esi + eax * 4]  ; Right child
    cmp ebx, edx
    jge no_right_child
    mov ebx, edx              ; Use right child index

no_right_child:
    mov edx, [esi + edi * 4]
    cmp edx, ebx
    jge heapify_done

    ; Swap
    mov [esi + edi * 4], ebx
    mov [esi + eax * 4], edx
    mov edi, eax
    jmp heapify_loop

heapify_done:
    pop edi edx ecx ebx eax
    ret
heapify endp

print_array proc
    push ecx esi
print_loop:
    mov eax, [esi]
    call print_int
    add esi, 4
    loop print_loop
    invoke StdOut, 13, 10
    pop esi ecx
    ret
print_array endp

; Integer to String Conversion
int_to_string proc
    ; Converts EAX into a null-terminated string at EDI
    push eax ebx ecx edx
    mov ecx, 10
    xor edx, edx
convert_loop:
    xor edx, edx
    div ecx
    add dl, '0'
    dec edi
    mov [edi], dl
    test eax, eax
    jnz convert_loop
    pop edx ecx ebx eax
    ret
int_to_string endp

; Print integer
print_int proc
    push eax
    lea edi, temp_buffer
    call int_to_string
    invoke StdOut, addr temp_buffer
    invoke StdOut, addr space

    pop eax
    ret
print_int endp

end start
