#ifndef _C_PAIR_LIST_H
#define _C_PAIR_LIST_H

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>
#include "Python.h"

typedef struct pair {
    PyObject  *identity;  // 8
    PyObject  *key;       // 8
    PyObject  *value;     // 8
    Py_hash_t  hash;      // 8 ssize_t
} pair_t;

typedef struct pair_list {
    pair_t *pairs;
    Py_ssize_t  capacity;
    Py_ssize_t  size;
} pair_list_t;


pair_list_t *pair_list_new();

Py_ssize_t pair_list_len();

void pair_list_free(pair_list_t *list);

int pair_list_add(pair_list_t *list, PyObject *identity, PyObject *key,
		  PyObject *value, Py_hash_t hash);

int pair_list_at(pair_list_t *list, size_t idx, pair_t *pair);

#endif
