#ifndef _DMOBJ_STRUCT_H_
#define _DMOBJ_STRUCT_H_
#include <stdio.h>
#include <string.h>

#define CWMP_NODE_NAME_LEN 256
#define CWMP_ACCESSLIST_STR_LEN 32
#define CWMP_COMMON_STR_LEN 32

#ifndef TRUE
#define TRUE 1
#endif

#ifndef FALSE
#define FALSE 0
#endif

#ifndef BOOL
typedef unsigned char BOOL;
#endif

#ifndef DM_UINT32
typedef unsigned int DM_UINT32;
#endif

#ifndef DM_SINT32
typedef int DM_SINT32;
#endif

typedef enum _data_type_e
{
    dBOOL = 0,
    dINT,
    dUNSIGNED,
    dSTRING,
    dFLOAT,
    dDOUBLE,
    dDATETIME,
    dUnknown,
}DATA_TYPE_E;

typedef enum _access_type_e
{
    READ_ONLY = 0,
    READ_WRITE = 1
}ACCESS_TYPE_E;

typedef enum _notify_type_e
{
    NOTIFY_NONE = 0,
    NOTIFY_ACTIVE = 1,
    NOTIFY_PASSIVE = 2
}NOTIFICATION_E;

typedef union
{
	char *value;
	BOOL boolval;
	DM_SINT32 ival;
	DM_UINT32 uval;
}DM_PARAM_VALUE_U;

typedef struct _range_s
{
    union
    {
        DM_SINT32 minSInt;
        DM_UINT32 minUInt;
        DM_UINT32 minStrLen;
    }min;

    union
    {
        DM_SINT32 maxSInt;
        DM_UINT32 maxUInt;
        DM_UINT32 maxStrLen;
    }max;

    char *StringRange;
}DM_VAL_RANGE_S;

typedef struct _dm_param_
{
    char               name[CWMP_NODE_NAME_LEN]; /* parameter name */
    char               accessList[CWMP_ACCESSLIST_STR_LEN];/* accessList name */
    ACCESS_TYPE_E      access;       /* read or write */
    DATA_TYPE_E        value_type;   /* value type */
    NOTIFICATION_E     notification; /* notification type */
    BOOL               valueChanged; /* value changed or not */
    BOOL               needReboot;   /* value changed need reboot */
    DM_PARAM_VALUE_U   value;        /* value content */
    DM_PARAM_VALUE_U   defvalue;     /* default value */
    char               valueRangeStr[CWMP_COMMON_STR_LEN];/* value ranges string */
}DM_PARAMETER_S;


typedef struct _dm_obj_
{
    char name[CWMP_NODE_NAME_LEN]; /* node name */
    unsigned int NumOfChildParameters;
    unsigned int NumOfChildObjects;
    struct _dm_obj_ **ChildObjs;
    struct _dm_param_ *ChildParams;
}DM_OBJ_S;


typedef DM_OBJ_S* DM_OBJ_LIST;

#endif /* _DMOBJ_STRUCT_H_ */

