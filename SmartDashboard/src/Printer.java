import javax.swing.JLabel;

import edu.wpi.first.smartdashboard.gui.StaticWidget;
import edu.wpi.first.smartdashboard.properties.Property;


public class Printer extends StaticWidget{
	static JLabel widthLabel    = new JLabel();
	static JLabel distanceLabel = new JLabel();
	static JLabel aimLabel 	 = new JLabel();
	JLabel targetLabel   = new JLabel();
	
	@Override
	public void init() {
			
		add(widthLabel);
		add(distanceLabel);
		add(aimLabel);
		add(targetLabel);
		
	}

	@Override
	public void propertyChanged(Property arg0) {
		
	}
	
	public static void refresh() {
		widthLabel.setText("WIDTH: " + Vision.width);
		distanceLabel.setText("DISTANCE: " + Vision.distance);
		aimLabel.setText("AIM COORDINATE: " + Vision.centerAim);
	} 

}
