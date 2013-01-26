import java.awt.Dimension;

import javax.swing.JLabel;

import edu.wpi.first.smartdashboard.camera.WPICameraExtension;
import edu.wpi.first.smartdashboard.robot.Robot;
import edu.wpi.first.wpijavacv.WPIBinaryImage;
import edu.wpi.first.wpijavacv.WPIColor;
import edu.wpi.first.wpijavacv.WPIColorImage;
import edu.wpi.first.wpijavacv.WPIContour;
import edu.wpi.first.wpijavacv.WPIImage;
import edu.wpi.first.wpijavacv.WPIPoint;
import edu.wpi.first.wpijavacv.WPIPolygon;
import edu.wpi.first.wpilibj.networking.NetworkTable;


public class Vision extends WPICameraExtension {
	//private static final long serialVersionUID = -7612889513919831857L;
	//public NetworkTable table = (NetworkTable) Robot.getTable();
	public JLabel widthLabel;
	public JLabel heightLabel;
	public JLabel distanceLabel;
	public JLabel centerLabel;
	public double width;
	public double distance;
	public double target;
	public double height;
	public double centerAim;
	
	
	private static double getLength(WPIPoint a, WPIPoint b)
	  {

	    int deltax = a.getX() - b.getX();

	    int deltay = a.getY() - b.getY();

	    
	    return Math.sqrt((deltax * deltax) + (deltay * deltay));
	  }
	
public WPIImage processImage(WPIColorImage image) {
		//table.setTeam(2557);
		
		
		WPIBinaryImage red = image.getRedChannel().getThreshold(64),

                green = image.getGreenChannel().getThreshold(64),
                blue = image.getRedChannel().getThreshold(64);

 
 /* Find the threshold of the image, where dark and light colors are clearly
   separated. */
 WPIBinaryImage threshold = red.getAnd(green).getAnd(blue);

 threshold.dilate(1);
 threshold.erode(1);
 
 WPIColorImage output = new WPIColorImage(threshold.getBufferedImage());

 
 WPIPolygon bestMatch = null;
 
 WPIContour[] contours = threshold.findContours();

 for(WPIContour contour : contours)
   {
     /* Approximate each polygon in the image. */
     WPIPolygon p = contour.approxPolygon(25);

     
     /* Make sure it's a convex quadrilaterial that doesn't take up most
       of the screen */
     if(p.isConvex() && p.getNumVertices() == 4 && p.getHeight() < 240)
       {

         WPIPoint[] points = p.getPoints();
         
         double side1 = getLength(points[0], points[1]);

         double side2 = getLength(points[1], points[2]);

         double side3 = getLength(points[2], points[3]);

         double side4 = getLength(points[3], points[0]);

         
         double ratio1 = Math.abs(Math.log(side1 / side3));

         double ratio2 = Math.abs(Math.log(side2 / side4));

         
         /* If the lengths of the top to bottom and left to right sides are
           very close, the shape is a rectangle */
         if(ratio1 < 0.1 && ratio2 < 0.1)
           {

             if(bestMatch == null || p.getHeight() < bestMatch.getHeight())

               bestMatch = p;
           }
       }
   }
 
 if(bestMatch != null)
   {

     image.drawPolygon(bestMatch, new WPIColor(0, 128, 255), 4);

     
     WPIPoint[] points = bestMatch.getPoints();
     
    

     double side1 = getLength(points[0], points[1]);

     double side2 = getLength(points[1], points[2]);

     
     /* Set the height to whichever side is shorter */
     if(side1 < side2) {
    	 height = side1;
    	 width  = side2;
     }

     else {
    	 width = side1;
    	 height = side2;
     }
     double FOVft = 320 * (4.5 / width); //full camera fov = 320pix * (width of target in ft/width of target in px)
     double tan24 = 0.45; //tangent of 24 degrees (half of the camera FOV)
     
     distance  = FOVft / tan24;  //calculates distance
     
     double centerPx  = points[1].getX() - (width/2); //gets pixel coordinate of center of target
     centerAim = 2 * (centerPx / 320 ) - 1; 
     
    /* table.beginTransaction();			//put values into networktable for robot to use
     table.putDouble("WIDTH", width);
     table.putDouble("CENTER", centerAim);
     table.putDouble("DISTANCE", distance);
     table.endTransaction();*/
     
     
     
     repaint();			//repaint panel
   
     setVisible(true);
     repaint();
     
		
		
	return image;
   }
 

widthLabel = new JLabel("Width: " + width);  	//add values to labels and print labels
heightLabel = new JLabel("Height: " + height);
distanceLabel = new JLabel("Distance: " + distance);
centerLabel = new JLabel("Target Coordinate: " + centerAim);
add(centerLabel);
add(widthLabel);
add(heightLabel);
add(distanceLabel);

return output;
		
	}
	
	

}

	
	

