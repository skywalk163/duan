/*
 * 段言 (Duan) 运行时库 - 完整版
 * 支持列表和字典操作
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// ====================================
// 列表实现（长度存储在数组头部）
// ====================================

// 列表结构：[长度][元素0][元素1]...
// 返回的指针指向数据部分，长度在 data[-1]

int* duan_list_new(long long size) {
    // 分配空间：1个int存储长度 + size个int存储数据
    int* buffer = (int*)malloc((size_t)(size + 1) * sizeof(int));
    if (!buffer) return NULL;
    buffer[0] = (int)size;  // 存储长度
    return buffer + 1;  // 返回数据部分的指针
}

int duan_list_length(int* list_ptr) {
    if (!list_ptr) return 0;
    return list_ptr[-1];  // 长度存储在数据前面
}

int duan_list_append(int* list_ptr, int value) {
    if (!list_ptr) return -1;
    
    int len = list_ptr[-1];
    // 需要重新分配空间
    int* new_buffer = (int*)realloc(list_ptr - 1, (len + 2) * sizeof(int));
    if (!new_buffer) return -1;
    
    list_ptr = new_buffer + 1;
    list_ptr[len] = value;
    list_ptr[-1] = len + 1;
    return len;
}

int duan_list_get(int* list_ptr, long long index) {
    if (!list_ptr) return 0;
    if (index < 0 || index >= list_ptr[-1]) return 0;
    return list_ptr[(int)index];
}

void duan_list_set(int* list_ptr, long long index, int value) {
    if (!list_ptr) return;
    if (index < 0 || index >= list_ptr[-1]) return;
    list_ptr[(int)index] = value;
}

int* duan_list_copy(int* list_ptr) {
    if (!list_ptr) return NULL;
    int len = list_ptr[-1];
    int* new_list = duan_list_new(len);
    if (!new_list) return NULL;
    memcpy(new_list, list_ptr, len * sizeof(int));
    return new_list;
}

void duan_list_free(int* list_ptr) {
    if (list_ptr) free(list_ptr - 1);
}

// ====================================
// 字典（哈希表）实现
// ====================================

#define HASH_SIZE 256

typedef struct DictEntry {
    char* key;
    int value;
    struct DictEntry* next;
} DictEntry;

typedef struct {
    DictEntry* table[HASH_SIZE];
} DuanDict;

unsigned int duan_dict_hash(const char* key) {
    unsigned int hash = 0;
    while (*key) {
        hash = (hash * 31) + *key++;
    }
    return hash % HASH_SIZE;
}

void* duan_dict_new() {
    DuanDict* dict = (DuanDict*)malloc(sizeof(DuanDict));
    if (!dict) return NULL;
    memset(dict->table, 0, sizeof(dict->table));
    return dict;
}

void duan_dict_set(void* dict_ptr, const char* key, int value) {
    DuanDict* dict = (DuanDict*)dict_ptr;
    if (!dict || !key) return;
    
    unsigned int index = duan_dict_hash(key);
    DictEntry* entry = dict->table[index];
    
    while (entry) {
        if (strcmp(entry->key, key) == 0) {
            entry->value = value;
            return;
        }
        entry = entry->next;
    }
    
    entry = (DictEntry*)malloc(sizeof(DictEntry));
    entry->key = strdup(key);
    entry->value = value;
    entry->next = dict->table[index];
    dict->table[index] = entry;
}

int duan_dict_get(void* dict_ptr, const char* key) {
    DuanDict* dict = (DuanDict*)dict_ptr;
    if (!dict || !key) return 0;
    
    unsigned int index = duan_dict_hash(key);
    DictEntry* entry = dict->table[index];
    
    while (entry) {
        if (strcmp(entry->key, key) == 0) {
            return entry->value;
        }
        entry = entry->next;
    }
    return 0;
}

_Bool duan_dict_contains(void* dict_ptr, const char* key) {
    DuanDict* dict = (DuanDict*)dict_ptr;
    if (!dict || !key) return 0;
    
    unsigned int index = duan_dict_hash(key);
    DictEntry* entry = dict->table[index];
    
    while (entry) {
        if (strcmp(entry->key, key) == 0) {
            return 1;
        }
        entry = entry->next;
    }
    return 0;
}

void duan_dict_remove(void* dict_ptr, const char* key) {
    DuanDict* dict = (DuanDict*)dict_ptr;
    if (!dict || !key) return;
    
    unsigned int index = duan_dict_hash(key);
    DictEntry** pp = &dict->table[index];
    DictEntry* entry = *pp;
    
    while (entry) {
        if (strcmp(entry->key, key) == 0) {
            *pp = entry->next;
            free(entry->key);
            free(entry);
            return;
        }
        pp = &entry->next;
        entry = *pp;
    }
}

void duan_dict_free(void* dict_ptr) {
    DuanDict* dict = (DuanDict*)dict_ptr;
    if (!dict) return;
    
    for (int i = 0; i < HASH_SIZE; i++) {
        DictEntry* entry = dict->table[i];
        while (entry) {
            DictEntry* next = entry->next;
            free(entry->key);
            free(entry);
            entry = next;
        }
    }
    free(dict);
}

// ====================================
// 类型转换函数
// ====================================

char* duan_itoa(int value) {
    static char buffer[20];
    sprintf(buffer, "%d", value);
    return buffer;
}