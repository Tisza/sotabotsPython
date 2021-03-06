import javax.swing.JLabel;

import edu.wpi.first.smartdashboard.gui.StaticWidget;
import edu.wpi.first.smartdashboard.properties.Property;
import edu.wpi.first.smartdashboard.robot.Robot;
import edu.wpi.first.wpilibj.networktables.*;



public class Printer extends StaticWidget{
	/**
	 * 
	 */
	private static final long serialVersionUID = 7049313544834323095L;
	static JLabel xLabel    = new JLabel();
	static JLabel distanceLabel = new JLabel();
	static JLabel aimLabel 	 = new JLabel();
	static JLabel targetLabel   = new JLabel();
	
	
	
	@Override
	public void init() {
		add(xLabel);
		add(distanceLabel);
		add(aimLabel);
		add(targetLabel);
		
	}

	@Override
	public void propertyChanged(Property arg0) {
		
	}
	
	public static void refresh() {
		distanceLabel.setText("DISTANCE" + Vision.distance);
		xLabel.setText("AVG DISTANCE: " + Vision.avgDistance);
		aimLabel.setText("AIM COORDINATE: " + Vision.centerAim);
		targetLabel.setText("AIM AVG: " + Vision.avgCenterAim);
                
                //NetworkTablesDesktopClient.run("DISTANCE", Vision.avgDistance);
                //NetworkTablesDesktopClient.run("AIM", Vision.avgCenterAim);
		
	} 
	

}
