/* C module to generate Fresnel arrays binary transmission in Numpy array */

#define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION
#include <Python.h>
#include <numpy/arrayobject.h>

// Define the boolean type non-recognized by C
// Coded with 1 byte (8-bit)
#define false 0
#define true  1
typedef unsigned char bool;

/*
Function allocating the necessary memory for a contiguous array of
booleans :
- nRows : lines number
- nCols : columns number
*/
bool* allocBoolArray2D(int nRows, int nCols)
{
	bool* array = malloc(nRows*nCols*sizeof(bool));
	if(!array)
	{
		return NULL;
	}
	return array;
}

/*
Defines the structure of a white ring :
- rInf : inferior radius
- rSup : superior radius
*/
struct Ring
{
    double rInf;
    double rSup;
} typedef Ring;

/*
Function to get the mask of the Fresnel array, unique function usable by
the compiled Python module :
- width :
- nZones :
- obstruction :
- offset :
- wavelength :
- size :
- beta0 :
*/
PyObject* getMask(PyObject* self, PyObject* args)
{
    double dWidth;
    int nZones;
    double dObstruction;
    double dOffset;
    double dWavelength;
    int nSize;
    double dBeta0;

    // Parses the parameters
    if (!PyArg_ParseTuple(args, "didddid", &dWidth, &nZones, &dObstruction,
    &dOffset, &dWavelength, &nSize, &dBeta0))
    {
        return NULL;
    }

	// Computes the Fresnel rings
    int nRingMax = 2 * nZones;
    Ring* rings = malloc(nRingMax*sizeof(Ring));
	if(!rings)
	{
		return NULL;
	}
    double dFocalLength = pow(dWidth / 2, 2) / (2 * nZones + dOffset - 0.75)
        /dWavelength;
    for(int i = 0; i < nRingMax; i++)
    {
        rings[i].rInf = sqrt(2 * dWavelength * dFocalLength * (i + dOffset -
        dBeta0) + pow(dWavelength * (i + dOffset - dBeta0), 2));
        rings[i].rSup = sqrt(2 * dWavelength * dFocalLength * (i + dOffset +
        dBeta0) + pow(dWavelength * (i + dOffset + dBeta0), 2));
    }

    // Computes the central square obstruction
    double dPixelWidth = dWidth / nSize;
    int nPixelObstruction = nSize / 2 - (int) (dObstruction / dPixelWidth /
    2.);

    // Makes the array
    bool* bArray = allocBoolArray2D(nSize, nSize);

    double xRef = (- dWidth + dPixelWidth) / 2;
    double yRef = (- dWidth + dPixelWidth) / 2;
    for(int i = 0; i < nSize / 2; i++)
    {
        for(int j = 0; j < nSize / 2; j++)
        {
            if(i >= nPixelObstruction && j >= nPixelObstruction)
            {
                bArray[i * nSize + j] = false;
                bArray[(i + 1) * nSize - 1 - j] = false;
                bArray[(nSize - 1 - i) * nSize + j] = false;
                bArray[(nSize - i) * nSize - 1 - j] = false;
            }
            else
            {
                double x = xRef + i * dPixelWidth;
                double y = yRef + j * dPixelWidth;
                double dDistance = sqrt(x * x + y * y);
                int k = nRingMax - 1;
                bool bFound = false;
                while(!bFound && k >= 0)
                {
                    if(dDistance >= rings[k].rSup)
                    {
                        bArray[i * nSize + j] = false;
                        bArray[(i + 1) * nSize - 1 - j] = false;
                        bArray[(nSize - 1 - i) * nSize + j] = false;
                        bArray[(nSize - i) * nSize - 1 - j] = false;
                        bFound = true;
                    }
                    else if(dDistance >= rings[k].rInf)
                    {
                        bArray[i * nSize + j] = true;
                        bArray[(i + 1) * nSize - 1 - j] = true;
                        bArray[(nSize - 1 - i) * nSize + j] = true;
                        bArray[(nSize - i) * nSize - 1 - j] = true;
                        bFound = true;
                    }
                    k--;
                }
                if(!bFound)
                {
                    bArray[i * nSize + j] = false;
                    bArray[(i + 1) * nSize - 1 - j] = false;
                    bArray[(nSize - 1 - i) * nSize + j] = false;
                    bArray[(nSize - i) * nSize - 1 - j] = false;
                }
            }
        }
    }

    // Computes the bars

    bool bEquidistant = true;
    double dBarThickness = 0.0002;
    double dBarSpace = 0.01;

    switch(bEquidistant)
    {
        case true :;
        double dBarDistance = rings[0].rInf;
        while(dBarDistance < dWidth / 2.)
        {
            double dBarInf = dBarDistance - dBarThickness / 2.;
            double dBarSup = dBarDistance + dBarThickness / 2.;

            int nBarInfFromCenter = (int) floor(dBarInf / dPixelWidth);
            int nBarSupFromCenter = (int) floor(dBarSup / dPixelWidth);

            int nFirstBarInf = nSize / 2. - 1 - nBarSupFromCenter;
            int nFirstBarSup = nSize / 2. - 1 - nBarInfFromCenter;
            int nSecondBarInf = nSize / 2. + nBarInfFromCenter;
            int nSecondBarSup = nSize / 2. + nBarSupFromCenter;

            // Full the left and right bar
            for(int i = 0; i < nSize; i++)
            {
                if((nFirstBarInf < i && i < nFirstBarSup) ||
                    (nSecondBarInf < i && i < nSecondBarSup))
                {
                    for(int j = 0; j < nSize; j++)
                    {
                        bArray[i * nSize + j] = false;
                    }
                }
                else
                {
                    for(int j = 0; j < nSize; j++)
                    {
                        if((nFirstBarInf < j && j < nFirstBarSup) ||
                            (nSecondBarInf < j && j < nSecondBarSup))
                        {
                            bArray[i * nSize + j] = false;
                        }
                    }
                }
            }
            dBarDistance += dBarSpace;
        }
        break;
    }

	// Writes the mask in a Python object to get a Numpy array
	PyArrayObject* c = NULL;
	npy_intp dim[2] = {nSize, nSize};
	c = (PyArrayObject*)PyArray_SimpleNewFromData(2, dim, NPY_BOOL, bArray);
    return (PyObject*)c;
}

/*
Defines functions in module :
- getMask : Generates the binary transmission of the Fresnel array
*/
static PyMethodDef Methods[] =
{
     {"get_mask", getMask, METH_VARARGS, "Generates the binary transmission"
     "of the Fresnel array"}
};

/*
Module initialization : fresnel_array_generator
*/
PyMODINIT_FUNC

initfresnel_array_generator(void)
{
	(void) Py_InitModule("fresnel_array_generator", Methods);
	import_array();
}
