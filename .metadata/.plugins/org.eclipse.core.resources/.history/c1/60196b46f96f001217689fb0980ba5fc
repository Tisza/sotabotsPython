package javajav;

public class CoorAverage {
	public static int index;
	public static int numSamples; //untested value
	public static double[] sampleArray;
	
	public CoorAverage () {
		index = 0;
		numSamples = 20;
		sampleArray = new double[numSamples];
		
		for (int i=0; i<sampleArray.length; i++) {
			sampleArray[i] = 0.00;
		}
	}
	
	public static double update(double x) {
		sampleArray[index] = x;
		index++;
		
		if (index > sampleArray.length - 1) {
				index = 0;
		}
		
		double sum = 0;

		
		for ( int i = 0; i < sampleArray.length - 1; i++ ) {
			sum += sampleArray[i];
		}
		
		return sum/(double)sampleArray.length;
	}


}