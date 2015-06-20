#include <stdio.h>
#include <string.h>

typedef union
{
	char *value;
	int ival;
	int boolval;
	unsigned int uval;
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
	char *name;
	int access;
	int value_type;
	int notification;
	int forcedInform;
	int valueChanged;
	DM_PARAM_VALUE_U value;
	DM_PARAM_VALUE_U defvalue;
	DM_VAL_RANGE_S valueRange;
	char accessList[64];
}DM_PARAMETER_S;

typedef struct _dm_obj_
{
	char *name;
	unsigned int NumOfChildParameters;
	unsigned int NumOfChildObjects;
	struct _dm_obj_ *ChildObjs;
	struct _dm_param_ *ChildParams;
}DM_OBJ_S;

