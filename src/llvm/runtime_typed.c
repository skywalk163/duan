/*
 * 段言 (Duan) 运行时库 - 类型版 (v3)
 * 
 * 基于 DuanValue 结构体，所有值携带类型标记。
 * 算术运算直接在原生类型上操作，避免 atoi/itoa 转换。
 * 
 * 类型系统：
 *   0 = NULL, 1 = INT, 2 = FLOAT, 3 = STRING, 4 = LIST, 5 = BOOL
 * 
 * 所有 DuanValue 参数通过指针传递，避免 C/LLVM 结构体布局 ABI 不兼容。
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <time.h>
#include <math.h>
#include <sys/stat.h>
#include <ctype.h>
#include <errno.h>

#ifdef _WIN32
#include <windows.h>
#include <io.h>
#include <direct.h>
#define F_OK 0
#define access _access
#else
#include <unistd.h>
#endif

/* ================================================================
 * 类型定义
 * ================================================================ */

typedef struct {
    int type;          /* 0=NULL 1=INT 2=FLOAT 3=STR 4=LIST 5=BOOL */
    int64_t i64;       /* INT */
    double f64;        /* FLOAT */
    char* str;         /* STR / LIST (序列化，仅用于 type=3) */
    int boolean;       /* BOOL */
    /* LIST 类型专用字段 (type=4) */
    int list_size;     /* 当前元素数量 */
    int list_capacity; /* 分配的数组容量 */
    struct DuanValue** list_data; /* 元素数组指针 */
} DuanValue;

/* ================================================================
 * 内部工具
 * ================================================================ */

static char* dv_strdup(const char* s) {
    if (!s) return NULL;
    size_t len = strlen(s);
    char* d = (char*)malloc(len + 1);
    if (d) memcpy(d, s, len + 1);
    return d;
}

/* ================================================================
 * 值构造器 - 写结果到 result 指针，避免返回 struct 值
 * ================================================================ */

void dv_null(DuanValue* result) {
    result->type = 0;
    result->i64 = 0;
    result->f64 = 0.0;
    result->str = NULL;
    result->boolean = 0;
}

int dv_is_null(DuanValue* v) {
    return v && v->type == 0;
}

/* null 合并操作符：如果 v 是 null，返回 default_val，否则返回 v */
void dv_null_coalesce(DuanValue* result, DuanValue* v, DuanValue* default_val) {
    if (v && v->type != 0) {
        dv_clone(result, v);
    } else {
        dv_clone(result, default_val);
    }
}

/* 安全获取属性：如果 obj 为 null，返回 null；否则返回 obj.属性 */
void dv_safe_get(DuanValue* result, DuanValue* obj, DuanValue* attr_name) {
    if (!obj || obj->type == 0) {
        dv_null(result);
        return;
    }
    if (obj->type == 6) {  /* OBJ 类型 */
        dv_class_get_member(result, obj, attr_name->str);
    } else {
        dv_null(result);
    }
}

void dv_int(DuanValue* result, int64_t x) {
    result->type = 1;
    result->i64 = x;
    result->f64 = 0.0;
    result->str = NULL;
    result->boolean = 0;
}

void dv_float(DuanValue* result, double x) {
    result->type = 2;
    result->i64 = 0;
    result->f64 = x;
    result->str = NULL;
    result->boolean = 0;
}

void dv_str(DuanValue* result, const char* s) {
    result->type = 3;
    result->i64 = 0;
    result->f64 = 0.0;
    result->str = dv_strdup(s ? s : "");
    result->boolean = 0;
}

void dv_bool(DuanValue* result, int b) {
    result->type = 5;
    result->i64 = 0;
    result->f64 = 0.0;
    result->str = NULL;
    result->boolean = b ? 1 : 0;
}

/* ================================================================
 * 值销毁 / 复制
 * ================================================================ */

void dv_free(DuanValue* v) {
    if (!v) return;
    if (v->type == 3 && v->str) {
        free(v->str);
        v->str = NULL;
    } else if (v->type == 4 && v->list_data) {
        for (int i = 0; i < v->list_size; i++) {
            if (v->list_data[i]) {
                dv_free(v->list_data[i]);
                free(v->list_data[i]);
            }
        }
        free(v->list_data);
        v->list_data = NULL;
        v->list_size = 0;
        v->list_capacity = 0;
    }
}

void dv_clone(DuanValue* result, DuanValue* v) {
    *result = *v;
    if (v->type == 3 && v->str) {
        result->str = dv_strdup(v->str);
    } else if (v->type == 4) {
        /* 复制列表数据 */
        result->list_data = NULL;
        result->list_size = 0;
        result->list_capacity = 0;
        if (v->list_size > 0 && v->list_data) {
            result->list_capacity = v->list_capacity > 0 ? v->list_capacity : v->list_size;
            result->list_data = (struct DuanValue**)malloc(result->list_capacity * sizeof(DuanValue*));
            for (int i = 0; i < v->list_size; i++) {
                if (v->list_data[i]) {
                    result->list_data[i] = (DuanValue*)malloc(sizeof(DuanValue));
                    dv_clone(result->list_data[i], v->list_data[i]);
                } else {
                    result->list_data[i] = NULL;
                }
            }
            result->list_size = v->list_size;
        }
    }
}

/* ================================================================
 * 类型转换 - 取 DuanValue* 避免 struct 传参 ABI 问题
 * ================================================================ */

int64_t dv_to_i64(DuanValue* v) {
    switch (v->type) {
        case 1: return v->i64;
        case 2: return (int64_t)v->f64;
        case 5: return v->boolean ? 1 : 0;
        case 3: return v->str ? atoll(v->str) : 0;
        default: return 0;
    }
}

double dv_to_f64(DuanValue* v) {
    switch (v->type) {
        case 1: return (double)v->i64;
        case 2: return v->f64;
        case 5: return v->boolean ? 1.0 : 0.0;
        case 3: return v->str ? atof(v->str) : 0.0;
        default: return 0.0;
    }
}

const char* dv_to_str(DuanValue* v) {
    switch (v->type) {
        case 3: return v->str ? v->str : "";
        default: return "";
    }
}

int dv_to_bool(DuanValue* v) {
    switch (v->type) {
        case 0: return 0;
        case 1: return v->i64 != 0;
        case 2: return v->f64 != 0.0;
        case 3: return v->str && v->str[0] != '\0';
        case 5: return v->boolean;
        case 4: return 1;  /* 非空列表为真 */
        default: return 0;
    }
}

char* dv_to_string(DuanValue* v) {
    /* 转换为可读字符串形式 */
    char buf[128];
    switch (v->type) {
        case 0: return dv_strdup("空");
        case 1: snprintf(buf, sizeof(buf), "%lld", (long long)v->i64); return dv_strdup(buf);
        case 2: snprintf(buf, sizeof(buf), "%g", v->f64); return dv_strdup(buf);
        case 3: return dv_strdup(v->str ? v->str : "");
        case 5: return dv_strdup(v->boolean ? "真" : "假");
        case 4: return dv_strdup(v->str ? v->str : "[]");
        default: return dv_strdup("");
    }
}

/* ================================================================
 * 算术运算（类型提升：int + float → float）
 * ================================================================ */

static int dv_promote(DuanValue* a, DuanValue* b) {
    return (a->type == 2 || b->type == 2) ? 2 : 1;
}

static int dv_is_object_str(const char* s) {
    if (!s) return 0;
    return strncmp(s, "obj:", 4) == 0;
}

void dv_add(DuanValue* result, DuanValue* a, DuanValue* b);
void dv_sub(DuanValue* result, DuanValue* a, DuanValue* b);
void dv_mul(DuanValue* result, DuanValue* a, DuanValue* b);
void dv_div(DuanValue* result, DuanValue* a, DuanValue* b);

static void dv_add_default(DuanValue* result, DuanValue* a, DuanValue* b) {
    /* 特殊：字符串拼接 */
    if (a->type == 3 || b->type == 3) {
        char* sa = dv_to_string(a);
        char* sb = dv_to_string(b);
        char* r = (char*)malloc(strlen(sa) + strlen(sb) + 1);
        if (r) { sprintf(r, "%s%s", sa, sb); }
        free(sa);
        free(sb);
        if (r) {
            result->type = 3;
            result->i64 = 0;
            result->f64 = 0.0;
            result->str = dv_strdup(r);
            result->boolean = 0;
        } else {
            result->type = 3;
            result->i64 = 0;
            result->f64 = 0.0;
            result->str = dv_strdup("");
            result->boolean = 0;
        }
        free(r);
        return;
    }
    if (dv_promote(a, b) == 2) {
        result->type = 2;
        result->i64 = 0;
        result->f64 = dv_to_f64(a) + dv_to_f64(b);
        result->str = NULL;
        result->boolean = 0;
        return;
    }
    result->type = 1;
    result->i64 = dv_to_i64(a) + dv_to_i64(b);
    result->f64 = 0.0;
    result->str = NULL;
    result->boolean = 0;
}

static void dv_sub_default(DuanValue* result, DuanValue* a, DuanValue* b) {
    if (dv_promote(a, b) == 2) {
        result->type = 2;
        result->i64 = 0;
        result->f64 = dv_to_f64(a) - dv_to_f64(b);
        result->str = NULL;
        result->boolean = 0;
        return;
    }
    result->type = 1;
    result->i64 = dv_to_i64(a) - dv_to_i64(b);
    result->f64 = 0.0;
    result->str = NULL;
    result->boolean = 0;
}

static void dv_mul_default(DuanValue* result, DuanValue* a, DuanValue* b) {
    if (dv_promote(a, b) == 2) {
        result->type = 2;
        result->i64 = 0;
        result->f64 = dv_to_f64(a) * dv_to_f64(b);
        result->str = NULL;
        result->boolean = 0;
        return;
    }
    result->type = 1;
    result->i64 = dv_to_i64(a) * dv_to_i64(b);
    result->f64 = 0.0;
    result->str = NULL;
    result->boolean = 0;
}

static void dv_div_default(DuanValue* result, DuanValue* a, DuanValue* b) {
    if (dv_promote(a, b) == 2) {
        double denom = dv_to_f64(b);
        if (denom == 0.0) {
            dv_null(result);
            return;
        }
        result->type = 2;
        result->i64 = 0;
        result->f64 = dv_to_f64(a) / denom;
        result->str = NULL;
        result->boolean = 0;
        return;
    }
    int64_t denom = dv_to_i64(b);
    if (denom == 0) {
        dv_null(result);
        return;
    }
    result->type = 1;
    result->i64 = dv_to_i64(a) / denom;
    result->f64 = 0.0;
    result->str = NULL;
    result->boolean = 0;
}

/* ================================================================
 * 数学函数
 * ================================================================ */

void dv_sin(DuanValue* result, DuanValue* a) {
    double x = dv_to_f64(a);
    result->type = 2;
    result->i64 = 0;
    result->f64 = sin(x);
    result->str = NULL;
    result->boolean = 0;
}

void dv_cos(DuanValue* result, DuanValue* a) {
    double x = dv_to_f64(a);
    result->type = 2;
    result->i64 = 0;
    result->f64 = cos(x);
    result->str = NULL;
    result->boolean = 0;
}

void dv_sqrt(DuanValue* result, DuanValue* a) {
    double x = dv_to_f64(a);
    if (x < 0) {
        dv_null(result);
        return;
    }
    result->type = 2;
    result->i64 = 0;
    result->f64 = sqrt(x);
    result->str = NULL;
    result->boolean = 0;
}

void dv_abs(DuanValue* result, DuanValue* a) {
    if (a->type == 1) {
        int64_t x = dv_to_i64(a);
        result->type = 1;
        result->i64 = x < 0 ? -x : x;
        result->f64 = 0.0;
        result->str = NULL;
        result->boolean = 0;
    } else {
        double x = dv_to_f64(a);
        result->type = 2;
        result->i64 = 0;
        result->f64 = fabs(x);
        result->str = NULL;
        result->boolean = 0;
    }
}

void dv_pow(DuanValue* result, DuanValue* a, DuanValue* b) {
    double x = dv_to_f64(a);
    double y = dv_to_f64(b);
    result->type = 2;
    result->i64 = 0;
    result->f64 = pow(x, y);
    result->str = NULL;
    result->boolean = 0;
}

void dv_floor(DuanValue* result, DuanValue* a) {
    if (a->type == 1) {
        dv_clone(result, a);
        return;
    }
    double x = dv_to_f64(a);
    result->type = 1;
    result->i64 = (int64_t)floor(x);
    result->f64 = 0.0;
    result->str = NULL;
    result->boolean = 0;
}

void dv_ceil(DuanValue* result, DuanValue* a) {
    if (a->type == 1) {
        dv_clone(result, a);
        return;
    }
    double x = dv_to_f64(a);
    result->type = 1;
    result->i64 = (int64_t)ceil(x);
    result->f64 = 0.0;
    result->str = NULL;
    result->boolean = 0;
}

void dv_mod(DuanValue* result, DuanValue* a, DuanValue* b) {
    if (a->type == 1 && b->type == 1) {
        int64_t x = dv_to_i64(a);
        int64_t y = dv_to_i64(b);
        if (y == 0) {
            dv_null(result);
            return;
        }
        result->type = 1;
        result->i64 = x % y;
        result->f64 = 0.0;
        result->str = NULL;
        result->boolean = 0;
    } else {
        double x = dv_to_f64(a);
        double y = dv_to_f64(b);
        if (y == 0.0) {
            dv_null(result);
            return;
        }
        result->type = 2;
        result->i64 = 0;
        result->f64 = fmod(x, y);
        result->str = NULL;
        result->boolean = 0;
    }
}

/* ================================================================
 * 比较运算
 * ================================================================ */

int dv_eq(DuanValue* a, DuanValue* b) {
    if (a->type == 3 && b->type == 3) {
        return (a->str && b->str && strcmp(a->str, b->str) == 0) ||
               (!a->str && !b->str);
    }
    if (a->type == 2 || b->type == 2) {
        return dv_to_f64(a) == dv_to_f64(b);
    }
    return dv_to_i64(a) == dv_to_i64(b);
}

int dv_cmp(DuanValue* a, DuanValue* b) {
    /* 返回 -1, 0, 1 用于 <, ==, > */
    if (a->type == 3 && b->type == 3) {
        if (!a->str && !b->str) return 0;
        if (!a->str) return -1;
        if (!b->str) return 1;
        return strcmp(a->str, b->str);
    }
    double fa = dv_to_f64(a);
    double fb = dv_to_f64(b);
    if (fa < fb) return -1;
    if (fa > fb) return 1;
    return 0;
}

int dv_lt(DuanValue* a, DuanValue* b) { return dv_cmp(a, b) < 0; }
int dv_gt(DuanValue* a, DuanValue* b) { return dv_cmp(a, b) > 0; }
int dv_le(DuanValue* a, DuanValue* b) { return dv_cmp(a, b) <= 0; }
int dv_ge(DuanValue* a, DuanValue* b) { return dv_cmp(a, b) >= 0; }

/* ================================================================
 * I/O 函数
 * ================================================================ */

void dv_print(DuanValue* v) {
    char* s = dv_to_string(v);
    if (s) printf("%s", s);
    free(s);
}

void dv_println(DuanValue* v) {
    char* s = dv_to_string(v);
    if (s) printf("%s\n", s);
    free(s);
}

void dv_print_int(DuanValue* result, int64_t n) {
    printf("%lld\n", (long long)n);
    result->type = 1;
    result->i64 = n;
    result->f64 = 0.0;
    result->str = NULL;
    result->boolean = 0;
}

void dv_input(DuanValue* result) {
    char buf[4096];
    if (fgets(buf, sizeof(buf), stdin)) {
        size_t len = strlen(buf);
        if (len > 0 && buf[len-1] == '\n') buf[len-1] = '\0';
        if (len > 1 && buf[len-2] == '\r') buf[len-2] = '\0';
        result->type = 3;
        result->i64 = 0;
        result->f64 = 0.0;
        result->str = dv_strdup(buf);
        result->boolean = 0;
        return;
    }
    result->type = 3;
    result->i64 = 0;
    result->f64 = 0.0;
    result->str = dv_strdup("");
    result->boolean = 0;
}

/* ================================================================
 * 字符串操作
 * ================================================================ */

void dv_concat(DuanValue* result, DuanValue* a, DuanValue* b) {
    char* sa = dv_to_string(a);
    char* sb = dv_to_string(b);
    char* r = (char*)malloc(strlen(sa) + strlen(sb) + 1);
    if (r) { sprintf(r, "%s%s", sa, sb); }
    free(sa);
    free(sb);
    if (r) {
        result->type = 3;
        result->i64 = 0;
        result->f64 = 0.0;
        result->str = dv_strdup(r);
        result->boolean = 0;
    } else {
        result->type = 3;
        result->i64 = 0;
        result->f64 = 0.0;
        result->str = dv_strdup("");
        result->boolean = 0;
    }
    free(r);
}

int64_t dv_str_len(DuanValue* v) {
    if (v->type == 3 && v->str) return (int64_t)strlen(v->str);
    return 0;
}

void dv_substr(DuanValue* result, DuanValue* str, int64_t start, int64_t len) {
    if (str->type != 3 || !str->str) {
        dv_str(result, "");
        return;
    }
    const char* s = str->str;
    int64_t slen = (int64_t)strlen(s);
    if (start < 0) start = slen + start;
    if (start < 0) start = 0;
    if (start >= slen) {
        dv_str(result, "");
        return;
    }
    if (len < 0) len = slen - start;
    if (start + len > slen) len = slen - start;
    char* out = (char*)malloc(len + 1);
    if (out) {
        memcpy(out, s + start, len);
        out[len] = '\0';
    }
    result->type = 3;
    result->i64 = 0;
    result->f64 = 0.0;
    result->str = out;
    result->boolean = 0;
}

int64_t dv_str_find(DuanValue* str, DuanValue* sub) {
    if (str->type != 3 || sub->type != 3 || !str->str || !sub->str) return -1;
    const char* found = strstr(str->str, sub->str);
    if (!found) return -1;
    return (int64_t)(found - str->str);
}

void dv_upper(DuanValue* result, DuanValue* str) {
    if (str->type != 3 || !str->str) {
        dv_str(result, "");
        return;
    }
    const char* s = str->str;
    int len = (int)strlen(s);
    char* out = (char*)malloc(len + 1);
    if (out) {
        for (int i = 0; i < len; i++) {
            out[i] = (char)toupper((unsigned char)s[i]);
        }
        out[len] = '\0';
    }
    result->type = 3;
    result->i64 = 0;
    result->f64 = 0.0;
    result->str = out;
    result->boolean = 0;
}

void dv_lower(DuanValue* result, DuanValue* str) {
    if (str->type != 3 || !str->str) {
        dv_str(result, "");
        return;
    }
    const char* s = str->str;
    int len = (int)strlen(s);
    char* out = (char*)malloc(len + 1);
    if (out) {
        for (int i = 0; i < len; i++) {
            out[i] = (char)tolower((unsigned char)s[i]);
        }
        out[len] = '\0';
    }
    result->type = 3;
    result->i64 = 0;
    result->f64 = 0.0;
    result->str = out;
    result->boolean = 0;
}

void dv_trim(DuanValue* result, DuanValue* str) {
    if (str->type != 3 || !str->str) {
        dv_str(result, "");
        return;
    }
    const char* s = str->str;
    int len = (int)strlen(s);
    int start = 0;
    int end = len - 1;
    while (start < len && isspace((unsigned char)s[start])) start++;
    while (end >= start && isspace((unsigned char)s[end])) end--;
    int out_len = end - start + 1;
    char* out = (char*)malloc(out_len + 1);
    if (out) {
        memcpy(out, s + start, out_len);
        out[out_len] = '\0';
    }
    result->type = 3;
    result->i64 = 0;
    result->f64 = 0.0;
    result->str = out;
    result->boolean = 0;
}

void dv_str_replace(DuanValue* result, DuanValue* str, DuanValue* old_s, DuanValue* new_s) {
    if (str->type != 3 || old_s->type != 3 || new_s->type != 3 || !str->str || !old_s->str || !new_s->str) {
        dv_str(result, "");
        return;
    }
    const char* s = str->str;
    const char* old_sub = old_s->str;
    const char* new_sub = new_s->str;
    int old_len = (int)strlen(old_sub);
    int new_len = (int)strlen(new_sub);
    if (old_len == 0) {
        dv_str(result, s);
        return;
    }
    int count = 0;
    const char* p = s;
    while ((p = strstr(p, old_sub)) != NULL) {
        count++;
        p += old_len;
    }
    int out_len = (int)strlen(s) + count * (new_len - old_len);
    char* out = (char*)malloc(out_len + 1);
    if (!out) {
        dv_str(result, "");
        return;
    }
    char* dst = out;
    p = s;
    while (1) {
        const char* found = strstr(p, old_sub);
        if (!found) {
            strcpy(dst, p);
            break;
        }
        memcpy(dst, p, found - p);
        dst += (found - p);
        memcpy(dst, new_sub, new_len);
        dst += new_len;
        p = found + old_len;
    }
    result->type = 3;
    result->i64 = 0;
    result->f64 = 0.0;
    result->str = out;
    result->boolean = 0;
}

/* ================================================================
 * 列表操作
 * ================================================================ */

/* 列表初始化辅助函数 */
static void dv_list_init_internal(DuanValue* result, int capacity) {
    result->type = 4;  /* LIST 类型 */
    result->i64 = 0;
    result->f64 = 0.0;
    result->str = NULL;
    result->boolean = 0;
    result->list_size = 0;
    result->list_capacity = capacity > 0 ? capacity : 4;
    result->list_data = (struct DuanValue**)malloc(result->list_capacity * sizeof(DuanValue*));
    for (int i = 0; i < result->list_capacity; i++) {
        result->list_data[i] = NULL;
    }
}

/* 列表增长辅助函数 */
static void dv_list_grow(DuanValue* list) {
    if (!list || list->type != 4) return;
    int new_capacity = list->list_capacity * 2;
    struct DuanValue** new_data = (struct DuanValue**)malloc(new_capacity * sizeof(DuanValue*));
    for (int i = 0; i < list->list_size; i++) {
        new_data[i] = list->list_data[i];
    }
    for (int i = list->list_size; i < new_capacity; i++) {
        new_data[i] = NULL;
    }
    free(list->list_data);
    list->list_data = new_data;
    list->list_capacity = new_capacity;
}

/* 列表添加元素辅助函数 */
static void dv_list_add_internal(DuanValue* list, DuanValue* elem) {
    if (!list || list->type != 4 || !elem) return;
    if (list->list_size >= list->list_capacity) {
        dv_list_grow(list);
    }
    if (list->list_size < list->list_capacity) {
        list->list_data[list->list_size] = elem;
        list->list_size++;
    }
}

void dv_list_new(DuanValue* result) {
    dv_list_init_internal(result, 4);
}

int64_t dv_list_len(DuanValue* v) {
    if (v->type != 4) return 0;
    return v->list_size;
}

int64_t dv_len(DuanValue* v) {
    if (v->type == 3) {
        const char* s = v->str ? v->str : "";
        if (strncmp(s, "dict:", 5) == 0) {
            return atoll(s + 5);
        }
        return (int64_t)strlen(s);
    }
    if (v->type == 4) {
        return v->list_size;
    }
    return 0;
}

void dv_list_get(DuanValue* result, DuanValue* list, int64_t index) {
    if (list->type != 4) {
        dv_null(result);
        return;
    }
    if (index < 0 || index >= list->list_size) {
        dv_null(result);
        return;
    }
    DuanValue* elem = list->list_data[index];
    if (elem) {
        dv_clone(result, elem);
    } else {
        dv_null(result);
    }
}

/* 列表操作：基于动态数组实现 */

void dv_list_append(DuanValue* result, DuanValue* list, DuanValue* elem) {
    if (!result) return;
    
    DuanValue* new_list;
    if (list->type == 4) {
        /* 复制原列表 */
        new_list = (DuanValue*)malloc(sizeof(DuanValue));
        if (!new_list) { dv_list_new(result); return; }
        dv_list_init_internal(new_list, list->list_capacity + 1);
        for (int i = 0; i < list->list_size; i++) {
            DuanValue* copy = (DuanValue*)malloc(sizeof(DuanValue));
            if (copy) {
                dv_clone(copy, list->list_data[i]);
                dv_list_add_internal(new_list, copy);
            }
        }
    } else {
        new_list = (DuanValue*)malloc(sizeof(DuanValue));
        if (!new_list) { dv_list_new(result); return; }
        dv_list_init_internal(new_list, 4);
    }
    
    /* 添加新元素 */
    DuanValue* elem_copy = (DuanValue*)malloc(sizeof(DuanValue));
    if (elem_copy) {
        dv_clone(elem_copy, elem);
        dv_list_add_internal(new_list, elem_copy);
    }
    
    result->type = 4;
    result->i64 = 0;
    result->f64 = 0.0;
    result->str = NULL;
    result->boolean = 0;
    result->list_size = new_list->list_size;
    result->list_capacity = new_list->list_capacity;
    result->list_data = new_list->list_data;
    free(new_list);
}

void dv_list_clear(DuanValue* result, DuanValue* list) {
    if (result == list) {
        /* 清空当前列表 */
        for (int i = 0; i < list->list_size; i++) {
            if (list->list_data[i]) {
                dv_free(list->list_data[i]);
                free(list->list_data[i]);
                list->list_data[i] = NULL;
            }
        }
        list->list_size = 0;
    } else {
        dv_list_new(result);
    }
}

void dv_list_set(DuanValue* result, DuanValue* list, int64_t index, DuanValue* elem) {
    if (list->type != 4 || index < 0 || index >= list->list_size) {
        dv_clone(result, list);
        return;
    }
    
    /* 复制列表 */
    DuanValue* new_list = (DuanValue*)malloc(sizeof(DuanValue));
    if (!new_list) { dv_clone(result, list); return; }
    
    dv_list_init_internal(new_list, list->list_capacity);
    for (int i = 0; i < list->list_size; i++) {
        DuanValue* copy = (DuanValue*)malloc(sizeof(DuanValue));
        if (i == index && elem) {
            dv_clone(copy, elem);
        } else {
            dv_clone(copy, list->list_data[i]);
        }
        dv_list_add_internal(new_list, copy);
    }
    
    result->type = 4;
    result->i64 = 0;
    result->f64 = 0.0;
    result->str = NULL;
    result->boolean = 0;
    result->list_size = new_list->list_size;
    result->list_capacity = new_list->list_capacity;
    result->list_data = new_list->list_data;
    free(new_list);
}

void dv_list_insert(DuanValue* result, DuanValue* list, int64_t index, DuanValue* elem) {
    if (list->type != 4) {
        dv_list_new(result);
        return;
    }
    
    if (index < 0) index = 0;
    if (index > list->list_size) index = list->list_size;
    
    /* 复制列表 */
    DuanValue* new_list = (DuanValue*)malloc(sizeof(DuanValue));
    if (!new_list) { dv_clone(result, list); return; }
    
    dv_list_init_internal(new_list, list->list_capacity + 1);
    for (int i = 0; i < list->list_size; i++) {
        if (i == index) {
            DuanValue* copy = (DuanValue*)malloc(sizeof(DuanValue));
            dv_clone(copy, elem);
            dv_list_add_internal(new_list, copy);
        }
        DuanValue* copy = (DuanValue*)malloc(sizeof(DuanValue));
        dv_clone(copy, list->list_data[i]);
        dv_list_add_internal(new_list, copy);
    }
    if (index >= list->list_size) {
        DuanValue* copy = (DuanValue*)malloc(sizeof(DuanValue));
        dv_clone(copy, elem);
        dv_list_add_internal(new_list, copy);
    }
    
    result->type = 4;
    result->i64 = 0;
    result->f64 = 0.0;
    result->str = NULL;
    result->boolean = 0;
    result->list_size = new_list->list_size;
    result->list_capacity = new_list->list_capacity;
    result->list_data = new_list->list_data;
    free(new_list);
}

void dv_list_remove(DuanValue* result, DuanValue* list, int64_t index) {
    if (list->type != 4 || index < 0 || index >= list->list_size) {
        dv_clone(result, list);
        return;
    }
    
    /* 复制列表（跳过要删除的元素） */
    DuanValue* new_list = (DuanValue*)malloc(sizeof(DuanValue));
    if (!new_list) { dv_clone(result, list); return; }
    
    dv_list_init_internal(new_list, list->list_capacity);
    for (int i = 0; i < list->list_size; i++) {
        if (i == index) continue;
        DuanValue* copy = (DuanValue*)malloc(sizeof(DuanValue));
        dv_clone(copy, list->list_data[i]);
        dv_list_add_internal(new_list, copy);
    }
    
    result->type = 4;
    result->i64 = 0;
    result->f64 = 0.0;
    result->str = NULL;
    result->boolean = 0;
    result->list_size = new_list->list_size;
    result->list_capacity = new_list->list_capacity;
    result->list_data = new_list->list_data;
    free(new_list);
}

int64_t dv_list_index_of(DuanValue* list, DuanValue* elem) {
    if (list->type != 4 || !elem) return -1;
    
    for (int i = 0; i < list->list_size; i++) {
        DuanValue* e = list->list_data[i];
        if (e && dv_eq(e, elem)) {
            return i;
        }
    }
    return -1;
}

int64_t dv_list_contains(DuanValue* list, DuanValue* elem) {
    return dv_list_index_of(list, elem) >= 0 ? 1 : 0;
}

void dv_list_reverse(DuanValue* result, DuanValue* list) {
    if (list->type != 4) {
        dv_list_new(result);
        return;
    }
    
    DuanValue* new_list = (DuanValue*)malloc(sizeof(DuanValue));
    if (!new_list) { dv_clone(result, list); return; }
    
    dv_list_init_internal(new_list, list->list_capacity);
    for (int i = list->list_size - 1; i >= 0; i--) {
        DuanValue* copy = (DuanValue*)malloc(sizeof(DuanValue));
        dv_clone(copy, list->list_data[i]);
        dv_list_add_internal(new_list, copy);
    }
    
    result->type = 4;
    result->i64 = 0;
    result->f64 = 0.0;
    result->str = NULL;
    result->boolean = 0;
    result->list_size = new_list->list_size;
    result->list_capacity = new_list->list_capacity;
    result->list_data = new_list->list_data;
    free(new_list);
}

static int cmp_dv(const void* a, const void* b) {
    DuanValue* va = *(DuanValue**)a;
    DuanValue* vb = *(DuanValue**)b;
    if (!va && !vb) return 0;
    if (!va) return -1;
    if (!vb) return 1;
    char* sa = dv_to_string(va);
    char* sb = dv_to_string(vb);
    int cmp = strcmp(sa ? sa : "", sb ? sb : "");
    free(sa);
    free(sb);
    return cmp;
}

void dv_list_sort(DuanValue* result, DuanValue* list) {
    if (list->type != 4 || list->list_size <= 1) {
        dv_clone(result, list);
        return;
    }
    
    DuanValue* new_list = (DuanValue*)malloc(sizeof(DuanValue));
    if (!new_list) { dv_clone(result, list); return; }
    
    dv_list_init_internal(new_list, list->list_capacity);
    for (int i = 0; i < list->list_size; i++) {
        DuanValue* copy = (DuanValue*)malloc(sizeof(DuanValue));
        dv_clone(copy, list->list_data[i]);
        dv_list_add_internal(new_list, copy);
    }
    
    qsort(new_list->list_data, new_list->list_size, sizeof(DuanValue*), cmp_dv);
    
    result->type = 4;
    result->i64 = 0;
    result->f64 = 0.0;
    result->str = NULL;
    result->boolean = 0;
    result->list_size = new_list->list_size;
    result->list_capacity = new_list->list_capacity;
    result->list_data = new_list->list_data;
    free(new_list);
}

void dv_str_split(DuanValue* result, DuanValue* str, DuanValue* delim) {
    if (str->type != 3 || delim->type != 3 || !str->str || !delim->str) {
        dv_list_new(result);
        return;
    }
    const char* s = str->str;
    const char* d = delim->str;
    int d_len = (int)strlen(d);
    
    int count = 1;
    const char* p = s;
    if (d_len > 0) {
        while ((p = strstr(p, d)) != NULL) {
            count++;
            p += d_len;
        }
    }
    
    /* 创建 type=4 的列表 */
    DuanValue* list = (DuanValue*)malloc(sizeof(DuanValue));
    if (!list) {
        dv_list_new(result);
        return;
    }
    dv_list_init_internal(list, count > 4 ? count : 4);
    
    p = s;
    for (int i = 0; i < count; i++) {
        const char* end;
        if (d_len > 0 && i < count - 1) {
            end = strstr(p, d);
        } else {
            end = p + strlen(p);
        }
        int part_len = (int)(end - p);
        char* part = (char*)malloc(part_len + 1);
        if (part) {
            memcpy(part, p, part_len);
            part[part_len] = '\0';
        }
        
        DuanValue* elem = (DuanValue*)malloc(sizeof(DuanValue));
        if (elem) {
            dv_str(elem, part ? part : "");
            dv_list_add_internal(list, elem);
        }
        if (part) free(part);
        p = end + d_len;
    }
    
    result->type = 4;
    result->i64 = 0;
    result->f64 = 0.0;
    result->str = NULL;
    result->boolean = 0;
    result->list_size = list->list_size;
    result->list_capacity = list->list_capacity;
    result->list_data = list->list_data;
    free(list);
}

/* ================================================================
 * 字典操作
 * 字典存储格式: "dict:N:key1\x1fvalue1\x1fkey2\x1fvalue2..."
 * 使用 \x1f (ASCII 31) 作为键值对分隔符
 * ================================================================ */

void dv_dict_new(DuanValue* result) {
    result->type = 3;  /* 复用 type=3，使用 str 字段存储 */
    result->i64 = 0;
    result->f64 = 0.0;
    result->str = dv_strdup("dict:0:");
    result->boolean = 0;
}

int64_t dv_dict_len(DuanValue* v) {
    if (v->type != 3 || !v->str) return 0;
    if (strncmp(v->str, "dict:", 5) != 0) return 0;
    return atoll(v->str + 5);
}

void dv_dict_set(DuanValue* result, DuanValue* dict, DuanValue* key, DuanValue* value) {
    if (dict->type != 3 || !dict->str || strncmp(dict->str, "dict:", 5) != 0) {
        dv_dict_new(result);
        return;
    }
    
    /* 将值转换为字符串以便存储 */
    DuanValue value_str;
    dv_value_to_string(&value_str, value);
    DuanValue key_str;
    dv_value_to_string(&key_str, key);
    
    const char* orig = dict->str;
    int64_t count = dv_dict_len(dict);
    
    /* 计算新字符串大小 */
    int key_len = (int)strlen(key_str.str);
    int val_len = (int)strlen(value_str.str);
    int buf_size = (int)strlen(orig) + key_len + val_len + 8;
    
    char* new_str = (char*)malloc(buf_size);
    if (!new_str) {
        dv_free(&value_str);
        dv_free(&key_str);
        dv_dict_new(result);
        return;
    }
    
    /* 构建新的字典字符串 */
    int pos = 0;
    pos += snprintf(new_str + pos, buf_size - pos, "dict:%lld:", (long long)(count + 1));
    
    /* 复制原有的键值对 */
    const char* p = orig + 5;
    p = strchr(p, ':');
    if (p) p++;
    for (int64_t i = 0; i < count; i++) {
        const char* key_start = p;
        const char* key_end = strstr(key_start, "\x1f");
        if (!key_end) break;
        int klen = (int)(key_end - key_start);
        
        const char* val_start = key_end + 1;
        const char* val_end = strstr(val_start, "\x1f");
        if (!val_end) val_end = val_start + strlen(val_start);
        int vlen = (int)(val_end - val_start);
        
        memcpy(new_str + pos, key_start, key_end - key_start);
        pos += key_end - key_start;
        new_str[pos++] = '\x1f';
        
        memcpy(new_str + pos, val_start, val_end - val_start);
        pos += val_end - val_start;
        new_str[pos++] = '\x1f';
        
        p = val_end;
        if (*p == '\x1f') p++;
    }
    
    /* 添加新的键值对 */
    memcpy(new_str + pos, key_str.str, key_len);
    pos += key_len;
    new_str[pos++] = '\x1f';
    memcpy(new_str + pos, value_str.str, val_len);
    pos += val_len;
    new_str[pos] = '\0';
    
    dv_free(&value_str);
    dv_free(&key_str);
    
    result->type = 3;
    result->i64 = 0;
    result->f64 = 0.0;
    result->str = new_str;
    result->boolean = 0;
}

void dv_dict_get(DuanValue* result, DuanValue* dict, DuanValue* key) {
    if (dict->type != 3 || !dict->str || strncmp(dict->str, "dict:", 5) != 0) {
        dv_null(result);
        return;
    }
    
    DuanValue key_str;
    dv_value_to_string(&key_str, key);
    
    const char* orig = dict->str;
    int64_t count = dv_dict_len(dict);
    
    const char* p = orig + 5;
    p = strchr(p, ':');
    if (p) p++;
    
    for (int64_t i = 0; i < count; i++) {
        const char* key_start = p;
        const char* key_end = strstr(key_start, "\x1f");
        if (!key_end) break;
        int klen = (int)(key_end - key_start);
        
        const char* val_start = key_end + 1;
        const char* val_end = strstr(val_start, "\x1f");
        if (!val_end) val_end = val_start + strlen(val_start);
        int vlen = (int)(val_end - val_start);
        
        if (klen == (int)strlen(key_str.str) && 
            strncmp(key_start, key_str.str, klen) == 0) {
            /* 找到匹配的键，返回值 */
            char* val_copy = (char*)malloc(vlen + 1);
            if (val_copy) {
                memcpy(val_copy, val_start, vlen);
                val_copy[vlen] = '\0';
            }
            dv_free(&key_str);
            dv_str(result, val_copy ? val_copy : "");
            if (val_copy) free(val_copy);
            return;
        }
        
        p = val_end;
        if (*p == '\x1f') p++;
    }
    
    dv_free(&key_str);
    dv_null(result);
}

void dv_dict_has(DuanValue* result, DuanValue* dict, DuanValue* key) {
    if (dict->type != 3 || !dict->str || strncmp(dict->str, "dict:", 5) != 0) {
        result->type = 5;
        result->i64 = 0;
        result->f64 = 0.0;
        result->boolean = 0;
        return;
    }
    
    DuanValue key_str;
    dv_value_to_string(&key_str, key);
    
    const char* orig = dict->str;
    int64_t count = dv_dict_len(dict);
    
    const char* p = orig + 5;
    p = strchr(p, ':');
    if (p) p++;
    
    int found = 0;
    for (int64_t i = 0; i < count && !found; i++) {
        const char* key_start = p;
        const char* key_end = strstr(key_start, "\x1f");
        if (!key_end) break;
        int klen = (int)(key_end - key_start);
        
        const char* val_start = key_end + 1;
        const char* val_end = strstr(val_start, "\x1f");
        if (!val_end) val_end = val_start + strlen(val_start);
        
        if (klen == (int)strlen(key_str.str) && 
            strncmp(key_start, key_str.str, klen) == 0) {
            found = 1;
        }
        
        p = val_end;
        if (*p == '\x1f') p++;
    }
    
    dv_free(&key_str);
    result->type = 5;
    result->i64 = 0;
    result->f64 = 0.0;
    result->boolean = found;
}

void dv_dict_keys(DuanValue* result, DuanValue* dict) {
    dv_list_new(result);
    if (dict->type != 3 || !dict->str || strncmp(dict->str, "dict:", 5) != 0) {
        return;
    }
    
    int64_t count = dv_dict_len(dict);
    const char* orig = dict->str;
    
    const char* p = orig + 5;
    p = strchr(p, ':');
    if (p) p++;
    
    for (int64_t i = 0; i < count; i++) {
        const char* key_start = p;
        const char* key_end = strstr(key_start, "\x1f");
        if (!key_end) break;
        int klen = (int)(key_end - key_start);
        
        char* key_copy = (char*)malloc(klen + 1);
        if (key_copy) {
            memcpy(key_copy, key_start, klen);
            key_copy[klen] = '\0';
        }
        
        DuanValue key_val;
        dv_str(&key_val, key_copy ? key_copy : "");
        if (key_copy) free(key_copy);
        
        DuanValue list_copy;
        dv_clone(&list_copy, result);
        dv_list_append(result, &list_copy, &key_val);
        dv_free(&list_copy);
        dv_free(&key_val);
        
        const char* val_start = key_end + 1;
        const char* val_end = strstr(val_start, "\x1f");
        if (!val_end) val_end = val_start + strlen(val_start);
        p = val_end;
        if (*p == '\x1f') p++;
    }
}

void dv_dict_values(DuanValue* result, DuanValue* dict) {
    dv_list_new(result);
    if (dict->type != 3 || !dict->str || strncmp(dict->str, "dict:", 5) != 0) {
        return;
    }
    
    int64_t count = dv_dict_len(dict);
    const char* orig = dict->str;
    
    const char* p = orig + 5;
    p = strchr(p, ':');
    if (p) p++;
    
    for (int64_t i = 0; i < count; i++) {
        const char* key_start = p;
        const char* key_end = strstr(key_start, "\x1f");
        if (!key_end) break;
        
        const char* val_start = key_end + 1;
        const char* val_end = strstr(val_start, "\x1f");
        if (!val_end) val_end = val_start + strlen(val_start);
        int vlen = (int)(val_end - val_start);
        
        char* val_copy = (char*)malloc(vlen + 1);
        if (val_copy) {
            memcpy(val_copy, val_start, vlen);
            val_copy[vlen] = '\0';
        }
        
        DuanValue val_val;
        dv_str(&val_val, val_copy ? val_copy : "");
        if (val_copy) free(val_copy);
        
        DuanValue list_copy;
        dv_clone(&list_copy, result);
        dv_list_append(result, &list_copy, &val_val);
        dv_free(&list_copy);
        dv_free(&val_val);
        
        p = val_end;
        if (*p == '\x1f') p++;
    }
}

void dv_dict_remove(DuanValue* result, DuanValue* dict, DuanValue* key) {
    /* 字典不支持删除操作，复制原字典 */
    dv_clone(result, dict);
}

/* ================================================================
 * 时间函数
 * ================================================================ */

double dv_timestamp(void) {
    return (double)time(NULL);
}

char* dv_format_time(double ts, const char* fmt) {
    if (!fmt) fmt = "%Y-%m-%d %H:%M:%S";
    time_t t = (time_t)ts;
    struct tm* tm_info = localtime(&t);
    char buffer[256];
    strftime(buffer, sizeof(buffer), fmt, tm_info);
    return dv_strdup(buffer);
}

/* ================================================================
 * 文件操作
 * ================================================================ */

int dv_file_exists(const char* path) {
    if (!path) return 0;
    return access(path, F_OK) == 0;
}

char* dv_read_file(const char* path) {
    if (!path) return dv_strdup("");
    FILE* f = fopen(path, "rb");
    if (!f) return dv_strdup("");
    fseek(f, 0, SEEK_END);
    long size = ftell(f);
    fseek(f, 0, SEEK_SET);
    char* buf = (char*)malloc(size + 1);
    if (buf) {
        fread(buf, 1, size, f);
        buf[size] = '\0';
    }
    fclose(f);
    return buf ? buf : dv_strdup("");
}

void dv_write_file(const char* path, const char* content) {
    if (!path || !content) return;
    FILE* f = fopen(path, "wb");
    if (f) {
        fwrite(content, 1, strlen(content), f);
        fclose(f);
    }
}

void dv_append_file(const char* path, const char* content) {
    if (!path || !content) return;
    FILE* f = fopen(path, "ab");
    if (f) {
        fwrite(content, 1, strlen(content), f);
        fclose(f);
    }
}

int64_t dv_file_size(const char* path) {
    if (!path) return 0;
    FILE* f = fopen(path, "rb");
    if (!f) return 0;
    fseek(f, 0, SEEK_END);
    long size = ftell(f);
    fclose(f);
    return (int64_t)size;
}

int dv_delete_file(const char* path) {
    if (!path) return -1;
    return remove(path);
}

#ifndef _WIN32
#include <dirent.h>
#endif

void dv_list_dir(DuanValue* result, const char* path) {
    dv_list_new(result);
    if (!path) return;
    
#ifdef _WIN32
    /* Windows 实现 */
    char search_path[1024];
    snprintf(search_path, sizeof(search_path), "%s\\*", path);
    WIN32_FIND_DATAA find_data;
    HANDLE hFind = FindFirstFileA(search_path, &find_data);
    if (hFind == INVALID_HANDLE_VALUE) return;
    
    do {
        if (strcmp(find_data.cFileName, ".") == 0 || strcmp(find_data.cFileName, "..") == 0) {
            continue;
        }
        DuanValue elem;
        dv_str(&elem, find_data.cFileName);
        DuanValue tmp;
        dv_list_append(&tmp, result, &elem);
        dv_free(result);
        dv_clone(result, &tmp);
        dv_free(&elem);
        dv_free(&tmp);
    } while (FindNextFileA(hFind, &find_data));
    
    FindClose(hFind);
#else
    /* POSIX 实现 */
    DIR* dir = opendir(path);
    if (!dir) return;
    
    struct dirent* entry;
    while ((entry = readdir(dir)) != NULL) {
        if (strcmp(entry->d_name, ".") == 0 || strcmp(entry->d_name, "..") == 0) {
            continue;
        }
        DuanValue elem;
        dv_str(&elem, entry->d_name);
        DuanValue tmp;
        dv_list_append(&tmp, result, &elem);
        dv_free(result);
        dv_clone(result, &tmp);
        dv_free(&elem);
        dv_free(&tmp);
    }
    closedir(dir);
#endif
}

/* ================================================================
 * JSON 操作
 * ================================================================ */

static char* list_to_json_inner(const char* list, int indent, int depth) {
    if (!list || strncmp(list, "list:", 5) != 0) return dv_strdup("[]");
    int len = atoi(list + 5);
    
    size_t est = 4;
    for (int i = 0; i < len; i++) {
        DuanValue list_val;
        DuanValue elem;
        dv_str(&list_val, list);
        dv_list_get(&elem, &list_val, i);
        char* es = dv_to_string(&elem);
        est += strlen(es) + 4;
        free(es);
        dv_free(&elem);
        dv_free(&list_val);
    }
    
    char* r = (char*)malloc(est + indent * 2 + 64);
    if (!r) return dv_strdup("[]");
    
    char* wp = r;
    *wp++ = '[';
    if (indent > 0) { *wp++ = '\n'; }
    
    const char* p = strchr(list + 5, ':');
    if (!p) { *wp++ = ']'; *wp = '\0'; return r; }
    p++;
    
    for (int i = 0; i < len; i++) {
        if (indent > 0) {
            for (int s = 0; s < indent; s++) *wp++ = ' ';
        }
        
        const char* end = strchr(p, '\x1f');
        if (!end) end = p + strlen(p);
        
        int is_num = 1;
        for (const char* c = p; c < end; c++) {
            if (*c != '-' && *c != '.' && (*c < '0' || *c > '9')) { is_num = 0; break; }
        }
        
        if (is_num && end > p && *p != '.') {
            size_t len = end - p;
            memcpy(wp, p, len); wp += len;
        } else {
            *wp++ = '"';
            size_t len = end - p;
            memcpy(wp, p, len); wp += len;
            *wp++ = '"';
        }
        
        if (i < len - 1) *wp++ = ',';
        if (indent > 0) *wp++ = '\n';
        p = (*end == '\x1f') ? end + 1 : end;
    }
    
    if (indent > 0 && len > 0) {
        for (int s = 0; s < indent - 2; s++) *wp++ = ' ';
    }
    *wp++ = ']';
    *wp = '\0';
    return r;
}

char* duan_list_to_json(const char* list, int indent) {
    return list_to_json_inner(list, indent, 0);
}

/* ================================================================
 * 系统操作
 * ================================================================ */

char* dv_getenv(const char* name) {
    if (!name) return dv_strdup("");
    const char* val = getenv(name);
    return dv_strdup(val ? val : "");
}

char* dv_str_join(const char* list, const char* sep) {
    if (!list || strncmp(list, "list:", 5) != 0) return dv_strdup("");
    
    const char* colon = strchr(list + 5, ':');
    if (!colon) return dv_strdup("");
    
    int64_t len = atoll(list + 5);
    if (len <= 0) return dv_strdup("");
    
    size_t sep_len = sep ? strlen(sep) : 0;
    size_t total = 0;
    const char* p = colon + 1;
    
    for (int64_t i = 0; i < len; i++) {
        const char* end = strchr(p, '\x1f');
        if (!end) end = p + strlen(p);
        total += (end - p);
        if (i < len - 1) total += sep_len;
        p = end + 1;
    }
    
    char* result = (char*)malloc(total + 1);
    if (!result) return dv_strdup("");
    
    char* wp = result;
    p = colon + 1;
    
    for (int64_t i = 0; i < len; i++) {
        const char* end = strchr(p, '\x1f');
        if (!end) end = p + strlen(p);
        size_t elen = end - p;
        memcpy(wp, p, elen);
        wp += elen;
        if (i < len - 1 && sep_len > 0) {
            memcpy(wp, sep, sep_len);
            wp += sep_len;
        }
        p = end + 1;
    }
    
    *wp = '\0';
    return result;
}

int dv_setenv(const char* name, const char* value) {
    if (!name || !value) return -1;
#ifdef _WIN32
    return _putenv_s(name, value) == 0 ? 0 : -1;
#else
    return setenv(name, value, 1);
#endif
}

char* dv_getcwd(void) {
    char buf[4096];
#ifdef _WIN32
    if (_getcwd(buf, sizeof(buf)) == NULL) return dv_strdup("");
#else
    if (getcwd(buf, sizeof(buf)) == NULL) return dv_strdup("");
#endif
    return dv_strdup(buf);
}

int dv_chdir(const char* path) {
    if (!path) return -1;
#ifdef _WIN32
    return _chdir(path);
#else
    return chdir(path);
#endif
}

int dv_system(const char* cmd) {
    if (!cmd) return -1;
    return system(cmd);
}

void dv_exit(int code) {
    exit(code);
}

static int _dv_argc = 0;
static char** _dv_argv = NULL;

void dv_init_args(int argc, char** argv) {
    _dv_argc = argc;
    _dv_argv = argv;
}

void dv_get_args(DuanValue* result) {
    dv_list_new(result);
    if (_dv_argc <= 0 || !_dv_argv) return;
    for (int i = 0; i < _dv_argc; i++) {
        DuanValue elem;
        dv_str(&elem, _dv_argv[i]);
        DuanValue tmp;
        dv_list_append(&tmp, result, &elem);
        dv_free(result);
        dv_clone(result, &tmp);
        dv_free(&elem);
        dv_free(&tmp);
    }
}

/* ================================================================
 * 异常处理 (Try/Catch/Throw)
 * ================================================================ */

#include <setjmp.h>

#define MAX_TRY_DEPTH 16
static jmp_buf __dv_jmp_bufs[MAX_TRY_DEPTH];
static int __dv_try_level = -1;
static char __dv_exception_str[1024];
static void* __dv_current_jmp_buf = NULL;  // 当前活跃的 jmp_buf

/* 调用栈追踪系统 */
#define MAX_CALL_STACK 64
#define MAX_STACK_ENTRY_LEN 128
typedef struct {
    char func_name[MAX_STACK_ENTRY_LEN];
    char file_name[MAX_STACK_ENTRY_LEN];
    int line_number;
} StackEntry;

static StackEntry __dv_call_stack[MAX_CALL_STACK];
static int __dv_call_stack_size = 0;

void dv_stack_push(const char* func_name, const char* file_name, int line_number) {
    if (__dv_call_stack_size < MAX_CALL_STACK) {
        StackEntry* entry = &__dv_call_stack[__dv_call_stack_size];
        strncpy(entry->func_name, func_name ? func_name : "unknown", MAX_STACK_ENTRY_LEN - 1);
        entry->func_name[MAX_STACK_ENTRY_LEN - 1] = '\0';
        strncpy(entry->file_name, file_name ? file_name : "", MAX_STACK_ENTRY_LEN - 1);
        entry->file_name[MAX_STACK_ENTRY_LEN - 1] = '\0';
        entry->line_number = line_number;
        __dv_call_stack_size++;
    }
}

void dv_stack_pop(void) {
    if (__dv_call_stack_size > 0) {
        __dv_call_stack_size--;
    }
}

int dv_get_stack_trace(char* buf, int buf_size) {
    if (!buf || buf_size <= 0) return 0;
    buf[0] = '\0';
    
    for (int i = __dv_call_stack_size - 1; i >= 0; i--) {
        StackEntry* entry = &__dv_call_stack[i];
        char entry_str[MAX_STACK_ENTRY_LEN * 2];
        if (entry->line_number > 0) {
            snprintf(entry_str, sizeof(entry_str), "    at %s (%s:%d)\n",
                    entry->func_name, entry->file_name, entry->line_number);
        } else {
            snprintf(entry_str, sizeof(entry_str), "    at %s\n", entry->func_name);
        }
        strncat(buf, entry_str, buf_size - strlen(buf) - 1);
    }
    return (int)strlen(buf);
}

int dv_get_stack_size(void) {
    return __dv_call_stack_size;
}

void dv_clear_stack_trace(void) {
    __dv_call_stack_size = 0;
}

void dv_try_enter(int* result, void* jmp_buf_ptr) {
    __dv_try_level++;
    if (__dv_try_level < MAX_TRY_DEPTH) {
        int r = setjmp(__dv_jmp_bufs[__dv_try_level]);
        *result = r;
        if (r != 0) {
            __dv_try_level--;
            return;
        }
    } else {
        *result = 0;
    }
}

void* dv_try_push(void) {
    __dv_try_level++;
    if (__dv_try_level >= MAX_TRY_DEPTH) {
        __dv_try_level--;
        return NULL;
    }
    return (void*)__dv_jmp_bufs[__dv_try_level];
}

int dv_setjmp_at_level(int level) {
    if (level < 0 || level >= MAX_TRY_DEPTH) return -1;
    return setjmp(__dv_jmp_bufs[level]);
}

void dv_try_pop(void) {
    if (__dv_try_level >= 0) {
        __dv_try_level--;
    }
}

void dv_try_end(void) {
    if (__dv_try_level >= 0) __dv_try_level--;
}

void dv_throw(DuanValue* exc) {
    if (__dv_try_level < 0 || __dv_try_level >= MAX_TRY_DEPTH) return;
    char* s = dv_to_string(exc);
    strncpy(__dv_exception_str, s ? s : "unknown", 1023);
    __dv_exception_str[1023] = '\0';
    free(s);
    int level = __dv_try_level;
    longjmp(__dv_jmp_bufs[level], 1);
}

char* dv_get_exception_str(void) {
    return __dv_exception_str;
}

void dv_clear_exception(void) {
    __dv_exception_str[0] = '\0';
}

/* ================================================================
 * 异常类系统（基于类系统的异常）
 * ================================================================ */

/* 前置声明和常量 */
#ifndef MAX_CLASS_NAME_LEN
#define MAX_CLASS_NAME_LEN 64
#endif
void dv_get_class_name(DuanValue* obj, char* buf, int buf_size);
int dv_is_object(DuanValue* v);
int dv_isinstance(DuanValue* obj, const char* class_name);
void dv_class_get_member(DuanValue* result, DuanValue* obj, const char* field_name);
void dv_class_set_member(DuanValue* obj, const char* field_name, DuanValue* value);
void dv_class_new_named(DuanValue* result, const char* class_name);  // 前向声明

static DuanValue __dv_current_exception_obj;
static int __dv_has_exception_obj = 0;

void dv_throw_exception(DuanValue* exception_obj) {
    /* 获取当前栈追踪 */
    char stack_trace[4096];
    dv_get_stack_trace(stack_trace, sizeof(stack_trace));
    
    /* 设置异常的栈追踪属性 */
    DuanValue stack_val;
    dv_str(&stack_val, stack_trace);
    dv_class_set_member(exception_obj, "栈追踪", &stack_val);
    dv_free(&stack_val);
    
    if (__dv_try_level < 0 || __dv_try_level >= MAX_TRY_DEPTH) {
        /* 没有 try 块，直接打印错误信息并退出 */
        char class_name[MAX_CLASS_NAME_LEN];
        dv_get_class_name(exception_obj, class_name, sizeof(class_name));
        
        DuanValue msg_val;
        dv_null(&msg_val);
        dv_class_get_member(&msg_val, exception_obj, "消息");
        char* msg_str = dv_to_string(&msg_val);
        
        fprintf(stderr, "未捕获的异常: %s: %s\n", 
                class_name[0] ? class_name : "未知异常",
                msg_str ? msg_str : "");
        if (stack_trace[0]) {
            fprintf(stderr, "调用栈:\n%s", stack_trace);
        }
        free(msg_str);
        dv_free(&msg_val);
        exit(1);
    }
    
    /* 保存异常对象 */
    dv_clone(&__dv_current_exception_obj, exception_obj);
    __dv_has_exception_obj = 1;
    
    /* 同时保存字符串形式，用于向后兼容 */
    char* s = dv_to_string(exception_obj);
    strncpy(__dv_exception_str, s ? s : "unknown", 1023);
    __dv_exception_str[1023] = '\0';
    free(s);
    
    int level = __dv_try_level;
    longjmp(__dv_jmp_bufs[level], 1);
}

/* 创建带原因的异常 */
void dv_create_exception_with_cause(DuanValue* result, const char* class_name, 
                                   const char* message, DuanValue* cause) {
    /* 先创建普通异常对象 */
    dv_class_new_named(result, class_name);
    
    /* 设置消息 */
    DuanValue msg_val;
    dv_str(&msg_val, message ? message : "");
    dv_class_set_member(result, "消息", &msg_val);
    dv_free(&msg_val);
    
    /* 如果有原因，设置原因属性 */
    if (cause) {
        DuanValue cause_clone;
        dv_clone(&cause_clone, cause);
        dv_class_set_member(result, "原因", &cause_clone);
        dv_free(&cause_clone);
    }
    
    /* 设置空栈追踪（稍后抛出时会填充） */
    DuanValue empty_stack;
    dv_str(&empty_stack, "");
    dv_class_set_member(result, "栈追踪", &empty_stack);
    dv_free(&empty_stack);
}

/* 获取异常的完整描述（包括原因链） */
int dv_exception_to_full_string(DuanValue* exception_obj, char* buf, int buf_size) {
    if (!buf || buf_size <= 0) return 0;
    buf[0] = '\0';
    
    DuanValue current_ex;
    dv_clone(&current_ex, exception_obj);
    
    int depth = 0;
    while (current_ex.type == 6 && dv_is_object(&current_ex)) {  // TYPE_OBJ
        if (depth > 0) {
            strncat(buf, "\n原因: ", buf_size - strlen(buf) - 1);
        }
        
        char class_name[MAX_CLASS_NAME_LEN];
        dv_get_class_name(&current_ex, class_name, sizeof(class_name));
        
        DuanValue msg_val;
        dv_null(&msg_val);
        dv_class_get_member(&msg_val, &current_ex, "消息");
        char* msg_str = dv_to_string(&msg_val);
        
        char ex_line[512];
        snprintf(ex_line, sizeof(ex_line), "%s: %s", 
                class_name[0] ? class_name : "异常",
                msg_str ? msg_str : "");
        strncat(buf, ex_line, buf_size - strlen(buf) - 1);
        
        free(msg_str);
        dv_free(&msg_val);
        
        /* 获取栈追踪 */
        DuanValue stack_val;
        dv_null(&stack_val);
        dv_class_get_member(&stack_val, &current_ex, "栈追踪");
        char* stack_str = dv_to_string(&stack_val);
        if (stack_str && stack_str[0]) {
            strncat(buf, "\n调用栈:\n", buf_size - strlen(buf) - 1);
            strncat(buf, stack_str, buf_size - strlen(buf) - 1);
        }
        free(stack_str);
        dv_free(&stack_val);
        
        /* 获取原因，继续循环 */
        DuanValue next_ex;
        dv_null(&next_ex);
        dv_class_get_member(&next_ex, &current_ex, "原因");
        
        dv_free(&current_ex);
        
        if (next_ex.type == 6 && dv_is_object(&next_ex)) {
            dv_clone(&current_ex, &next_ex);
            dv_free(&next_ex);
            depth++;
        } else {
            dv_free(&next_ex);
            break;
        }
        
        if (depth > 10) break;  // 防止循环引用
    }
    
    dv_free(&current_ex);
    return (int)strlen(buf);
}

void dv_get_current_exception(DuanValue* result) {
    if (__dv_has_exception_obj) {
        dv_clone(result, &__dv_current_exception_obj);
    } else {
        dv_str(result, __dv_exception_str);
    }
}

int dv_exception_match(DuanValue* ex, const char* type_name) {
    if (!ex || !type_name) return 0;
    
    /* 如果是对象，使用 isinstance 检查 */
    if (dv_is_object(ex)) {
        return dv_isinstance(ex, type_name);
    }
    
    /* 字符串异常：特殊处理，匹配 "异常" 或 "Exception" */
    if (ex->type == 3 && ex->str) {
        if (strcmp(type_name, "异常") == 0 || strcmp(type_name, "Exception") == 0) {
            return 1;
        }
    }
    
    return 0;
}

void dv_clear_exception_obj(void) {
    if (__dv_has_exception_obj) {
        dv_free(&__dv_current_exception_obj);
        __dv_has_exception_obj = 0;
    }
    __dv_exception_str[0] = '\0';
}

/* 转换为字符串 */
/* ================================================================
 * 类型转换
 * ================================================================ */

void dv_to_int(DuanValue* result, DuanValue* v) {
    if (v->type == 1) {
        dv_clone(result, v);
        return;
    }
    if (v->type == 2) {
        result->type = 1;
        result->i64 = (int64_t)v->f64;
        result->f64 = 0.0;
        result->str = NULL;
        result->boolean = 0;
        return;
    }
    if (v->type == 3 && v->str) {
        int64_t val = 0;
        if (v->str[0] == '-' || v->str[0] == '+') {
            int sign = (v->str[0] == '-') ? -1 : 1;
            val = 0;
            for (const char* p = v->str + 1; *p; p++) {
                if (*p >= '0' && *p <= '9') {
                    val = val * 10 + (*p - '0');
                } else {
                    break;
                }
            }
            val *= sign;
        } else {
            val = 0;
            for (const char* p = v->str; *p; p++) {
                if (*p >= '0' && *p <= '9') {
                    val = val * 10 + (*p - '0');
                } else {
                    break;
                }
            }
        }
        result->type = 1;
        result->i64 = val;
        result->f64 = 0.0;
        result->str = NULL;
        result->boolean = 0;
        return;
    }
    result->type = 1;
    result->i64 = 0;
    result->f64 = 0.0;
    result->str = NULL;
    result->boolean = 0;
}

void dv_to_float(DuanValue* result, DuanValue* v) {
    if (v->type == 2) {
        dv_clone(result, v);
        return;
    }
    if (v->type == 1) {
        result->type = 2;
        result->i64 = 0;
        result->f64 = (double)v->i64;
        result->str = NULL;
        result->boolean = 0;
        return;
    }
    if (v->type == 3 && v->str) {
        double val = 0.0;
        int i = 0;
        int sign = 1;
        if (v->str[0] == '-') {
            sign = -1;
            i = 1;
        } else if (v->str[0] == '+') {
            i = 1;
        }
        for (; v->str[i]; i++) {
            if (v->str[i] >= '0' && v->str[i] <= '9') {
                val = val * 10 + (v->str[i] - '0');
            } else if (v->str[i] == '.') {
                double frac = 0.1;
                i++;
                for (; v->str[i]; i++) {
                    if (v->str[i] >= '0' && v->str[i] <= '9') {
                        val += (v->str[i] - '0') * frac;
                        frac *= 0.1;
                    } else {
                        break;
                    }
                }
                break;
            } else {
                break;
            }
        }
        result->type = 2;
        result->i64 = 0;
        result->f64 = val * sign;
        result->str = NULL;
        result->boolean = 0;
        return;
    }
    result->type = 2;
    result->i64 = 0;
    result->f64 = 0.0;
    result->str = NULL;
    result->boolean = 0;
}

void dv_to_bool_val(DuanValue* result, DuanValue* v) {
    int b = dv_to_bool(v);
    result->type = 5;
    result->i64 = 0;
    result->f64 = 0.0;
    result->str = NULL;
    result->boolean = b;
}

void dv_value_to_string(DuanValue* result, DuanValue* v) {
    char* s = dv_to_string(v);
    result->type = 3;
    result->i64 = 0;
    result->f64 = 0.0;
    result->str = dv_strdup(s ? s : "");
    result->boolean = 0;
    free(s);
}

/* ================================================================
 * 类 / 对象支持
 * ================================================================ */

/* 对象内部表示: "obj:field1\x1evalue1\x1efield2\x1evalue2..." */
#define OBJ_PREFIX "obj:"

void dv_class_new(DuanValue* result, int num_fields) {
    char prefix[32];
    snprintf(prefix, sizeof(prefix), "%s%d:", OBJ_PREFIX, num_fields);
    result->type = 3;
    result->i64 = 0;
    result->f64 = 0.0;
    result->str = dv_strdup(prefix);
    result->boolean = 0;
}

void dv_class_set_member(DuanValue* obj, const char* field_name, DuanValue* value) {
    if (!obj || obj->type != 3 || !obj->str) return;
    if (strncmp(obj->str, OBJ_PREFIX, strlen(OBJ_PREFIX)) != 0) return;
    
    char* field_str = dv_to_string(value);
    size_t field_name_len = strlen(field_name);
    size_t field_str_len = strlen(field_str);
    
    const char* data_start = obj->str + strlen(OBJ_PREFIX);
    const char* p = data_start;
    
    /* 查找字段是否已存在 */
    char search[512];
    size_t search_len = field_name_len + 1;
    if (search_len >= sizeof(search)) {
        free(field_str);
        return;
    }
    memcpy(search, field_name, field_name_len);
    search[field_name_len] = '\x1F';
    
    const char* found = strstr(p, search);
    int field_exists = (found != NULL);
    
    if (field_exists) {
        /* 字段已存在，更新其值 */
        const char* val_start = found + search_len;
        const char* val_end = strchr(val_start, '\x1F');
        if (!val_end) val_end = val_start + strlen(val_start);
        
        size_t old_val_len = val_end - val_start;
        size_t before_len = val_start - obj->str;
        size_t after_len = strlen(val_end);
        
        size_t new_len = before_len + field_str_len + after_len + 1;
        char* new_str = (char*)malloc(new_len);
        if (new_str) {
            memcpy(new_str, obj->str, before_len);
            memcpy(new_str + before_len, field_str, field_str_len);
            memcpy(new_str + before_len + field_str_len, val_end, after_len);
            new_str[before_len + field_str_len + after_len] = '\0';
            free(obj->str);
            obj->str = new_str;
        }
    } else {
        /* 字段不存在，追加 */
        size_t new_len = strlen(obj->str) + field_name_len + field_str_len + 3;
        char* new_str = (char*)malloc(new_len);
        if (new_str) {
            size_t pos = 0;
            memcpy(new_str + pos, obj->str, strlen(obj->str));
            pos += strlen(obj->str);
            memcpy(new_str + pos, field_name, field_name_len);
            pos += field_name_len;
            new_str[pos++] = '\x1F';
            memcpy(new_str + pos, field_str, field_str_len);
            pos += field_str_len;
            new_str[pos++] = '\x1F';
            new_str[pos] = '\0';
            free(obj->str);
            obj->str = new_str;
        }
    }
    free(field_str);
}

void dv_class_get_member(DuanValue* result, DuanValue* obj, const char* field_name) {
    if (!obj || obj->type != 3 || !obj->str) {
        dv_str(result, "");
        return;
    }
    if (strncmp(obj->str, OBJ_PREFIX, strlen(OBJ_PREFIX)) != 0) {
        dv_str(result, "");
        return;
    }
    
    /* 查找 field_name\x1Evalue\x1E */
    const char* p = obj->str + strlen(OBJ_PREFIX);
    char search[256];
    snprintf(search, sizeof(search), "%s%c", field_name, '\x1F');
    
    const char* found = strstr(p, search);
    if (!found) {
        dv_str(result, "");
        return;
    }
    
    found += strlen(search);
    const char* end = strchr(found, '\x1F');
    if (!end) end = found + strlen(found);
    
    size_t len = end - found;
    char* val = (char*)malloc(len + 1);
    if (val) {
        memcpy(val, found, len);
        val[len] = '\0';
        
        /* 检测类型并返回 */
        int is_int = 1, is_float = 0, dot = 0;
        int neg = (len > 0 && val[0] == '-') ? 1 : 0;
        for (size_t i = neg; i < len; i++) {
            if (val[i] < '0' || val[i] > '9') { is_int = 0; break; }
        }
        if (is_int && len > (size_t)neg) {
            result->type = 1;
            result->i64 = atoll(val);
            result->f64 = 0.0;
            result->str = NULL;
            result->boolean = 0;
            free(val);
            return;
        }
        neg = (len > 0 && val[0] == '-') ? 1 : 0;
        for (size_t i = neg; i < len; i++) {
            if (val[i] == '.') { dot++; continue; }
            if (val[i] < '0' || val[i] > '9') { is_float = 0; break; }
            is_float = 1;
        }
        if (is_float && dot == 1) {
            result->type = 2;
            result->i64 = 0;
            result->f64 = atof(val);
            result->str = NULL;
            result->boolean = 0;
            free(val);
            return;
        }
        result->type = 3;
        result->i64 = 0;
        result->f64 = 0.0;
        result->str = val;
        result->boolean = 0;
        return;
    }
    dv_str(result, "");
}

/* ================================================================
 * 类元信息系统
 * ================================================================ */

#define MAX_CLASS_NAME_LEN 64
#define CLASS_FIELD_PREFIX "__class__"
#define CLASS_FIELD_PREFIX_LEN 9  /* strlen("__class__") */
#define MAX_INHERIT_DEPTH 32

#define MAX_CLASSES 128
#define MAX_METHODS_PER_CLASS 64
#define MAX_ATTRS_PER_CLASS 128

typedef struct {
    char name[MAX_CLASS_NAME_LEN];
    char super_name[MAX_CLASS_NAME_LEN];
    int num_methods;
    char method_names[MAX_METHODS_PER_CLASS][MAX_CLASS_NAME_LEN];
    void* method_ptrs[MAX_METHODS_PER_CLASS];
    int method_flags[MAX_METHODS_PER_CLASS];  /* 0=实例方法, 1=类方法, 2=静态方法 */
    int num_attrs;
    char attr_names[MAX_ATTRS_PER_CLASS][MAX_CLASS_NAME_LEN];
} DuanClassInfo;

static DuanClassInfo __dv_classes[MAX_CLASSES];
static int __dv_num_classes = 0;

/* 前置声明 */
DuanClassInfo* dv_find_class(const char* name);

/* 注册类，返回类索引，失败返回 -1 */
int dv_register_class(const char* name, const char* super_name) {
    if (!name || !name[0]) return -1;
    if (__dv_num_classes >= MAX_CLASSES) return -1;
    
    /* 检查是否已存在 */
    DuanClassInfo* existing = dv_find_class(name);
    if (existing) {
        return (int)(existing - __dv_classes);
    }
    
    DuanClassInfo* cls = &__dv_classes[__dv_num_classes];
    memset(cls, 0, sizeof(DuanClassInfo));
    strncpy(cls->name, name, MAX_CLASS_NAME_LEN - 1);
    cls->name[MAX_CLASS_NAME_LEN - 1] = '\0';
    if (super_name && super_name[0]) {
        strncpy(cls->super_name, super_name, MAX_CLASS_NAME_LEN - 1);
        cls->super_name[MAX_CLASS_NAME_LEN - 1] = '\0';
    }
    cls->num_methods = 0;
    cls->num_attrs = 0;
    
    __dv_num_classes++;
    return __dv_num_classes - 1;
}

/* 按名查找类，找不到返回 NULL */
DuanClassInfo* dv_find_class(const char* name) {
    if (!name || !name[0]) return NULL;
    for (int i = 0; i < __dv_num_classes; i++) {
        if (strcmp(__dv_classes[i].name, name) == 0) {
            return &__dv_classes[i];
        }
    }
    return NULL;
}

/* 注册方法（内部通用函数），method_flag: 0=实例方法, 1=类方法, 2=静态方法 */
static int dv_register_method_internal(const char* class_name, const char* method_name, void* func_ptr, int method_flag) {
    if (!class_name || !method_name || !func_ptr) return -1;
    
    DuanClassInfo* cls = dv_find_class(class_name);
    if (!cls) return -1;
    if (cls->num_methods >= MAX_METHODS_PER_CLASS) return -1;
    
    /* 检查方法是否已存在 */
    for (int i = 0; i < cls->num_methods; i++) {
        if (strcmp(cls->method_names[i], method_name) == 0) {
            cls->method_ptrs[i] = func_ptr;
            cls->method_flags[i] = method_flag;
            return 0;
        }
    }
    
    strncpy(cls->method_names[cls->num_methods], method_name, MAX_CLASS_NAME_LEN - 1);
    cls->method_names[cls->num_methods][MAX_CLASS_NAME_LEN - 1] = '\0';
    cls->method_ptrs[cls->num_methods] = func_ptr;
    cls->method_flags[cls->num_methods] = method_flag;
    cls->num_methods++;
    return 0;
}

/* 注册实例方法，成功返回 0，失败返回 -1 */
int dv_register_method(const char* class_name, const char* method_name, void* func_ptr) {
    return dv_register_method_internal(class_name, method_name, func_ptr, 0);
}

/* 注册类方法，成功返回 0，失败返回 -1 */
int dv_register_class_method(const char* class_name, const char* method_name, void* func_ptr) {
    return dv_register_method_internal(class_name, method_name, func_ptr, 1);
}

/* 注册静态方法，成功返回 0，失败返回 -1 */
int dv_register_static_method(const char* class_name, const char* method_name, void* func_ptr) {
    return dv_register_method_internal(class_name, method_name, func_ptr, 2);
}

/* 内部辅助：递归查找方法（带深度限制） */
static void* dv_find_method_inner(const char* class_name, const char* method_name, int depth) {
    if (!class_name || !method_name) return NULL;
    if (depth > MAX_INHERIT_DEPTH) return NULL;
    
    DuanClassInfo* cls = dv_find_class(class_name);
    if (!cls) return NULL;
    
    /* 在当前类中查找 */
    for (int i = 0; i < cls->num_methods; i++) {
        if (strcmp(cls->method_names[i], method_name) == 0) {
            return cls->method_ptrs[i];
        }
    }
    
    /* 递归查找父类 */
    if (cls->super_name[0] != '\0') {
        return dv_find_method_inner(cls->super_name, method_name, depth + 1);
    }
    
    return NULL;
}

/* 查找方法（递归查找父类），找不到返回 NULL */
void* dv_find_method(const char* class_name, const char* method_name) {
    return dv_find_method_inner(class_name, method_name, 0);
}

/* 注册属性，成功返回 0，失败返回 -1 */
int dv_register_attr(const char* class_name, const char* attr_name) {
    if (!class_name || !attr_name) return -1;
    
    DuanClassInfo* cls = dv_find_class(class_name);
    if (!cls) return -1;
    if (cls->num_attrs >= MAX_ATTRS_PER_CLASS) return -1;
    
    /* 检查属性是否已存在 */
    for (int i = 0; i < cls->num_attrs; i++) {
        if (strcmp(cls->attr_names[i], attr_name) == 0) {
            return 0;
        }
    }
    
    strncpy(cls->attr_names[cls->num_attrs], attr_name, MAX_CLASS_NAME_LEN - 1);
    cls->attr_names[cls->num_attrs][MAX_CLASS_NAME_LEN - 1] = '\0';
    cls->num_attrs++;
    return 0;
}

/* 内部辅助：递归收集父类所有属性（带深度限制） */
static void collect_all_attrs_inner(const char* class_name, char attrs[][MAX_CLASS_NAME_LEN], int* count, int depth) {
    if (!class_name || !class_name[0] || !attrs || !count) return;
    if (depth > MAX_INHERIT_DEPTH) return;
    
    DuanClassInfo* cls = dv_find_class(class_name);
    if (!cls) return;
    
    /* 先递归收集父类属性 */
    if (cls->super_name[0] != '\0') {
        collect_all_attrs_inner(cls->super_name, attrs, count, depth + 1);
    }
    
    /* 添加当前类的属性（去重） */
    for (int i = 0; i < cls->num_attrs; i++) {
        int found = 0;
        for (int j = 0; j < *count; j++) {
            if (strcmp(attrs[j], cls->attr_names[i]) == 0) {
                found = 1;
                break;
            }
        }
        if (!found && *count < MAX_ATTRS_PER_CLASS) {
            strncpy(attrs[*count], cls->attr_names[i], MAX_CLASS_NAME_LEN - 1);
            attrs[*count][MAX_CLASS_NAME_LEN - 1] = '\0';
            (*count)++;
        }
    }
}

/* 递归收集父类所有属性 */
static void collect_all_attrs(const char* class_name, char attrs[][MAX_CLASS_NAME_LEN], int* count) {
    collect_all_attrs_inner(class_name, attrs, count, 0);
}

/* 带类名的对象创建 */
void dv_class_new_named(DuanValue* result, const char* class_name) {
    if (!result || !class_name || !class_name[0]) {
        dv_str(result, "");
        return;
    }
    
    char safe_name[MAX_CLASS_NAME_LEN];
    size_t name_len = strlen(class_name);
    if (name_len > MAX_CLASS_NAME_LEN - 1) name_len = MAX_CLASS_NAME_LEN - 1;
    memcpy(safe_name, class_name, name_len);
    safe_name[name_len] = '\0';
    
    /* 收集所有属性 */
    char all_attrs[MAX_ATTRS_PER_CLASS][MAX_CLASS_NAME_LEN];
    int num_all_attrs = 0;
    memset(all_attrs, 0, sizeof(all_attrs));
    collect_all_attrs(safe_name, all_attrs, &num_all_attrs);
    
    /* 计算字符串长度：
       "obj:__class__\x1fClassName\x1fattr1\x1f\x1fattr2\x1f\x1f..."
    */
    size_t total_len = strlen(OBJ_PREFIX) + CLASS_FIELD_PREFIX_LEN + 1 + name_len + 1; /* "__class__" + \x1f + class_name + \x1f */
    for (int i = 0; i < num_all_attrs; i++) {
        total_len += strlen(all_attrs[i]) + 2; /* attr + \x1f + \x1f */
    }
    total_len += 1; /* 终止符 */
    
    char* buf = (char*)malloc(total_len);
    if (!buf) {
        dv_str(result, "");
        return;
    }
    
    /* 构建对象字符串 */
    size_t pos = 0;
    memcpy(buf + pos, OBJ_PREFIX, strlen(OBJ_PREFIX));
    pos += strlen(OBJ_PREFIX);
    
    /* 添加 __class__ 字段 */
    memcpy(buf + pos, CLASS_FIELD_PREFIX, CLASS_FIELD_PREFIX_LEN);
    pos += CLASS_FIELD_PREFIX_LEN;
    buf[pos++] = '\x1F';
    memcpy(buf + pos, safe_name, name_len);
    pos += name_len;
    buf[pos++] = '\x1F';
    
    /* 添加所有属性，初始值为空 */
    for (int i = 0; i < num_all_attrs; i++) {
        memcpy(buf + pos, all_attrs[i], strlen(all_attrs[i]));
        pos += strlen(all_attrs[i]);
        buf[pos++] = '\x1F';
        buf[pos++] = '\x1F';
    }
    
    buf[pos] = '\0';
    
    result->type = 3;
    result->i64 = 0;
    result->f64 = 0.0;
    result->str = buf;
    result->boolean = 0;
}

/* 获取对象类名 */
void dv_get_class_name(DuanValue* obj, char* buf, int buf_size) {
    if (!buf || buf_size <= 0) return;
    buf[0] = '\0';
    
    if (!obj || obj->type != 3 || !obj->str) return;
    if (strncmp(obj->str, OBJ_PREFIX, strlen(OBJ_PREFIX)) != 0) return;
    
    const char* p = obj->str + strlen(OBJ_PREFIX);
    
    /* 构建 "__class__\x1f" 用于比较 */
    char class_field[CLASS_FIELD_PREFIX_LEN + 2];
    memcpy(class_field, CLASS_FIELD_PREFIX, CLASS_FIELD_PREFIX_LEN);
    class_field[CLASS_FIELD_PREFIX_LEN] = '\x1f';
    class_field[CLASS_FIELD_PREFIX_LEN + 1] = '\0';
    size_t class_field_len = CLASS_FIELD_PREFIX_LEN + 1;
    
    if (strncmp(p, class_field, class_field_len) != 0) {
        return;
    }
    
    const char* class_start = p + class_field_len;
    const char* end = strchr(class_start, '\x1F');
    if (!end) end = class_start + strlen(class_start);
    
    size_t len = end - class_start;
    if (len > (size_t)(buf_size - 1)) len = (size_t)(buf_size - 1);
    memcpy(buf, class_start, len);
    buf[len] = '\0';
}

/* 方法函数指针类型 */
typedef void (*DuanMethodFunc)(DuanValue* result, DuanValue* self, DuanValue* args, int num_args);

/* 调用对象方法 */
void dv_call_method(DuanValue* result, DuanValue* obj, const char* method_name, DuanValue* args, int num_args) {
    if (!result || !obj || !method_name) {
        if (result) dv_null(result);
        return;
    }
    
    char class_name[MAX_CLASS_NAME_LEN];
    dv_get_class_name(obj, class_name, sizeof(class_name));
    
    if (!class_name[0]) {
        dv_null(result);
        return;
    }
    
    void* func_ptr = dv_find_method(class_name, method_name);
    if (!func_ptr) {
        dv_null(result);
        return;
    }
    
    DuanMethodFunc method = (DuanMethodFunc)func_ptr;
    method(result, obj, args, num_args);
}

/* 调用父类方法（从指定类的父类开始查找） */
void dv_call_super_method(DuanValue* result, DuanValue* obj, const char* class_name, const char* method_name, DuanValue* args, int num_args) {
    if (!result || !obj || !class_name || !method_name) {
        if (result) dv_null(result);
        return;
    }
    
    DuanClassInfo* cls = dv_find_class(class_name);
    if (!cls || cls->super_name[0] == '\0') {
        dv_null(result);
        return;
    }
    
    void* func_ptr = dv_find_method(cls->super_name, method_name);
    if (!func_ptr) {
        dv_null(result);
        return;
    }
    
    DuanMethodFunc method = (DuanMethodFunc)func_ptr;
    method(result, obj, args, num_args);
}

/* 内部辅助：递归查找方法及类型（带深度限制） */
static void* dv_find_method_with_flag_inner(const char* class_name, const char* method_name, int* out_flag, int depth) {
    if (!class_name || !method_name) return NULL;
    if (depth > MAX_INHERIT_DEPTH) return NULL;
    
    DuanClassInfo* cls = dv_find_class(class_name);
    if (!cls) return NULL;
    
    /* 在当前类中查找 */
    for (int i = 0; i < cls->num_methods; i++) {
        if (strcmp(cls->method_names[i], method_name) == 0) {
            if (out_flag) *out_flag = cls->method_flags[i];
            return cls->method_ptrs[i];
        }
    }
    
    /* 递归查找父类 */
    if (cls->super_name[0] != '\0') {
        return dv_find_method_with_flag_inner(cls->super_name, method_name, out_flag, depth + 1);
    }
    
    return NULL;
}

/* 查找方法并返回类型，找不到返回 NULL */
static void* dv_find_method_with_flag(const char* class_name, const char* method_name, int* out_flag) {
    return dv_find_method_with_flag_inner(class_name, method_name, out_flag, 0);
}

/* 类方法函数指针类型：第一个参数是类名（字符串DuanValue*） */
typedef void (*DuanClassMethodFunc)(DuanValue* result, DuanValue* cls_val, DuanValue* args, int num_args);

/* 静态方法函数指针类型：没有 self/cls 参数 */
typedef void (*DuanStaticMethodFunc)(DuanValue* result, DuanValue* args, int num_args);

/* 调用类方法（通过类名调用） */
void dv_call_class_method(DuanValue* result, const char* class_name, const char* method_name, DuanValue* args, int num_args) {
    if (!result || !class_name || !method_name) {
        if (result) dv_null(result);
        return;
    }
    
    int method_flag = 0;
    void* func_ptr = dv_find_method_with_flag(class_name, method_name, &method_flag);
    if (!func_ptr) {
        dv_null(result);
        return;
    }
    
    /* 构建类值（用字符串表示类对象，内容为类名） */
    DuanValue cls_val;
    dv_str(&cls_val, class_name);
    
    if (method_flag == 1) {
        /* 类方法：签名 void func(result, cls_val, args, num_args) */
        DuanClassMethodFunc method = (DuanClassMethodFunc)func_ptr;
        method(result, &cls_val, args, num_args);
    } else if (method_flag == 2) {
        /* 静态方法：签名 void func(result, args, num_args) */
        DuanStaticMethodFunc method = (DuanStaticMethodFunc)func_ptr;
        method(result, args, num_args);
    } else {
        /* 实例方法不能通过类名直接调用，返回空 */
        dv_null(result);
    }
    
    dv_free(&cls_val);
}

/* 调用静态方法（通过类名调用） */
void dv_call_static_method(DuanValue* result, const char* class_name, const char* method_name, DuanValue* args, int num_args) {
    if (!result || !class_name || !method_name) {
        if (result) dv_null(result);
        return;
    }
    
    int method_flag = 0;
    void* func_ptr = dv_find_method_with_flag(class_name, method_name, &method_flag);
    if (!func_ptr) {
        dv_null(result);
        return;
    }
    
    if (method_flag == 2) {
        /* 静态方法：签名 void func(result, args, num_args) */
        DuanStaticMethodFunc method = (DuanStaticMethodFunc)func_ptr;
        method(result, args, num_args);
    } else if (method_flag == 1) {
        /* 类方法也可以通过静态方式调用，传入类名 */
        DuanValue cls_val;
        dv_str(&cls_val, class_name);
        DuanClassMethodFunc method = (DuanClassMethodFunc)func_ptr;
        method(result, &cls_val, args, num_args);
        dv_free(&cls_val);
    } else {
        /* 实例方法不能通过类名直接调用，返回空 */
        dv_null(result);
    }
}

/* ================================================================
 * 运算符重载支持
 * ================================================================ */

static int dv_is_object(DuanValue* v) {
    if (!v || v->type != 3 || !v->str) return 0;
    return strncmp(v->str, OBJ_PREFIX, strlen(OBJ_PREFIX)) == 0;
}

static int dv_try_operator_overload(DuanValue* result, DuanValue* a, DuanValue* b, const char* op_name_cn, const char* op_name_en) {
    if (!dv_is_object(a)) return 0;
    
    char class_name[MAX_CLASS_NAME_LEN];
    dv_get_class_name(a, class_name, sizeof(class_name));
    if (!class_name[0]) return 0;
    
    void* func_ptr = dv_find_method(class_name, op_name_cn);
    if (!func_ptr) {
        func_ptr = dv_find_method(class_name, op_name_en);
    }
    if (!func_ptr) return 0;
    
    DuanValue args[1];
    dv_clone(&args[0], b);
    
    DuanMethodFunc method = (DuanMethodFunc)func_ptr;
    method(result, a, args, 1);
    
    dv_free(&args[0]);
    return 1;
}

void dv_add(DuanValue* result, DuanValue* a, DuanValue* b) {
    if (dv_try_operator_overload(result, a, b, "加", "__add__")) {
        return;
    }
    dv_add_default(result, a, b);
}

void dv_sub(DuanValue* result, DuanValue* a, DuanValue* b) {
    if (dv_try_operator_overload(result, a, b, "减", "__sub__")) {
        return;
    }
    dv_sub_default(result, a, b);
}

void dv_mul(DuanValue* result, DuanValue* a, DuanValue* b) {
    if (dv_try_operator_overload(result, a, b, "乘", "__mul__")) {
        return;
    }
    dv_mul_default(result, a, b);
}

void dv_div(DuanValue* result, DuanValue* a, DuanValue* b) {
    if (dv_try_operator_overload(result, a, b, "除", "__div__")) {
        return;
    }
    dv_div_default(result, a, b);
}

/* ================================================================
 * 类型判断与 isinstance
 * ================================================================ */

static int dv_isinstance_inner(const char* class_name, const char* target_class, int depth) {
    if (!class_name || !target_class) return 0;
    if (depth > MAX_INHERIT_DEPTH) return 0;
    
    if (strcmp(class_name, target_class) == 0) {
        return 1;
    }
    
    DuanClassInfo* cls = dv_find_class(class_name);
    if (!cls) return 0;
    
    if (cls->super_name[0] != '\0') {
        return dv_isinstance_inner(cls->super_name, target_class, depth + 1);
    }
    
    return 0;
}

int dv_isinstance(DuanValue* obj, const char* class_name) {
    if (!obj || !class_name || !class_name[0]) return 0;
    
    if (obj->type != 3 || !obj->str) return 0;
    if (strncmp(obj->str, OBJ_PREFIX, strlen(OBJ_PREFIX)) != 0) return 0;
    
    char obj_class[MAX_CLASS_NAME_LEN];
    dv_get_class_name(obj, obj_class, sizeof(obj_class));
    
    if (!obj_class[0]) return 0;
    
    return dv_isinstance_inner(obj_class, class_name, 0);
}

void dv_get_type_name(DuanValue* obj, char* buf, int buf_size) {
    if (!buf || buf_size <= 0) return;
    buf[0] = '\0';
    
    if (!obj) return;
    
    switch (obj->type) {
        case 0:
            strncpy(buf, "空", buf_size - 1);
            buf[buf_size - 1] = '\0';
            break;
        case 1:
            strncpy(buf, "整数", buf_size - 1);
            buf[buf_size - 1] = '\0';
            break;
        case 2:
            strncpy(buf, "浮点数", buf_size - 1);
            buf[buf_size - 1] = '\0';
            break;
        case 3:
            if (obj->str && strncmp(obj->str, OBJ_PREFIX, strlen(OBJ_PREFIX)) == 0) {
                dv_get_class_name(obj, buf, buf_size);
            } else if (obj->str && strncmp(obj->str, "list:", 5) == 0) {
                strncpy(buf, "列表", buf_size - 1);
                buf[buf_size - 1] = '\0';
            } else {
                strncpy(buf, "文本", buf_size - 1);
                buf[buf_size - 1] = '\0';
            }
            break;
        case 4:
            strncpy(buf, "列表", buf_size - 1);
            buf[buf_size - 1] = '\0';
            break;
        case 5:
            strncpy(buf, "布尔", buf_size - 1);
            buf[buf_size - 1] = '\0';
            break;
        default:
            strncpy(buf, "未知", buf_size - 1);
            buf[buf_size - 1] = '\0';
            break;
    }
}
