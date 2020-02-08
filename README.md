# MyocardicalStrainMeasurement
Program to manually track myocardium landmarks in short axis cardiac MR images using Python and OpenCV


## Background and relevant literature
Heart is a very vital organ in the human body. It is responsible for continuous circulation of blood to all the organs of the body. Therefore, the heart primarily acts as a pump. The motion and dynamics of the different regions of the heart have a very strong impact on its pumping efficiency. In short, the dynamics of heart motion during systole and diastole is a major factor indicative of cardiac health. Therefore, in the recent years, Myocardial strain measurement has gained increasing traction from the cardiovascular research community. 


* Bilchick, K.C., Dimaano, V., Wu, K.C., Helm, R.H., Weiss, R.G., Lima, J.A., Berger, R.D., Tomaselli, G.F., Bluemke, D.A., Halperin, H.R. and Abraham, T., 2008. Cardiac magnetic resonance assessment of dyssynchrony and myocardial scar predicts function class improvement following cardiac resynchronization therapy. JACC: Cardiovascular Imaging, 1(5), pp.561-568.

* Albert C Lardo, Theodore P Abraham, and David A Kass, “Magnetic resonance imaging assessment of ventricular dyssynchrony: current and emerging concepts,”Journal of the American College of Cardiology, vol. 46,no. 12, pp. 2223–2228, 2005

## Aim and overview
The aim of the current project is to develop a simple program to enable manual extraction and tracking of individual myocardial segments from multi slice stack of 2D short-axis (SAX) cine MRI images. Long term aims of the project are -
  * to facilitate a ground truth generation for myocardial strain measurements, which would be later used for comparative     assessment of sophisticated tracking algorithms 
  * gaining insights into the accuracy of already existing products on CircleCVI and other commercial software packages.
