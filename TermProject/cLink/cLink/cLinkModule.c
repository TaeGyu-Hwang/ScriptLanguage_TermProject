#include <Python.h>
#include <math.h>

#ifndef M_PI
#define M_PI 3.14159265358979323846
#endif

double deg2rad(double deg) {
    return deg * (M_PI / 180);
}

static PyObject* calculate_distance(PyObject* self, PyObject* args) {
    double lat1, lon1, lat2, lon2;
    if (!PyArg_ParseTuple(args, "dddd", &lat1, &lon1, &lat2, &lon2)) {
        return NULL;
    }

    double dLat = deg2rad(lat2 - lat1);
    double dLon = deg2rad(lon2 - lon1);
    double a = sin(dLat / 2) * sin(dLat / 2) +
        cos(deg2rad(lat1)) * cos(deg2rad(lat2)) *
        sin(dLon / 2) * sin(dLon / 2);
    double c = 2 * atan2(sqrt(a), sqrt(1 - a));
    double distance = 6371.0 * c;

    return Py_BuildValue("d", distance);
}

static PyMethodDef DistanceMethods[] = {
    {"calculate_distance", calculate_distance, METH_VARARGS, "Calculate the distance between two points."},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef distancemodule = {
    PyModuleDef_HEAD_INIT,
    "cLink",
    NULL,
    -1,
    DistanceMethods
};

PyMODINIT_FUNC PyInit_cLink(void) {
    return PyModule_Create(&distancemodule);
}
