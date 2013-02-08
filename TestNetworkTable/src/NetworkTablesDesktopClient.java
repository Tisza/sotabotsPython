import edu.wpi.first.smartdashboard.robot.Robot;
import edu.wpi.first.wpilibj.networktables.NetworkTable;

public class NetworkTablesDesktopClient {

	/**
	 * @param args
	 */
	

	static void run( String key, double value ) {
                NetworkTable.setClientMode();
		NetworkTable.setIPAddress("10.25.57.2"); //sets our team number
		NetworkTable table = NetworkTable.getTable("SmartDashboard"); 
		
			
			table.putNumber(key, value); //puts the number "11" into a key called "Q"
			
				
		}
		
	}


