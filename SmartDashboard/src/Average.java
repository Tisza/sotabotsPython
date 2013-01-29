import java.text.DecimalFormat;
import java.util.ArrayList;


public class Average {
	public static int index = 0;
	public static int numSamples = 150; //untested value
	public static double[] sampleArray = new double[numSamples];
	public static DecimalFormat df = new DecimalFormat("##.##");
	public static int sum = 0;
	
	public static double update(double x) {
		sampleArray[index] = x;
		index++;
		
		if (index >= numSamples) {
				index = 0;
		}
		
		for ( int i = 0; i < sampleArray.length; i++ ) {
			sum += sampleArray[i];
		}
		
		double average = Double.parseDouble(df.format(sum / sampleArray.length));
		return average;
	}

}
