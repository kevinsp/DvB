package de.virtuelleBaustelle.activities;

import de.virtuelleBaustelle.misc.Settings;
import de.virtuelleBaustelle.R;

import android.os.Bundle;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.graphics.Matrix;
import android.view.LayoutInflater;
import android.view.MotionEvent;
import android.view.View;
import android.view.View.OnTouchListener;
import android.view.ViewGroup;
import android.view.ViewTreeObserver.OnGlobalLayoutListener;
import android.widget.ImageView;

public class MotionFragment extends RemoteFragment {
	private final String MSG_TAG = "MOVE";
	
	//TURNSWITCH-STUFF
	private Bitmap tsOriginal, tsScaled;
	private Matrix tsMatrix;
	private int tsHeight, tsWidth;
	private ImageView iv_turnSwitch, iv_dPad;
		
	//MOTION-DECLARATIONS
	private final static int RIGHT		= 1, LEFT 		= -1;
	private final static int FORWARD	= 1, BACKWARD 	= -1;
	private final static int CLOCK		= 1, ANTICLOCK 	= -1;
	private final static int POISE = 0;
	
	private final static int[] poise = new int[]{0,0,0,0,0};
	
	//RELEVANT SETTING_VALUES
	private final static float  stillDpad		 	  = Settings.getSensitivityDpad();
	private final static double sensitivityTurnSwitch = Settings.getTurnswitchInhibition();
	
	@Override
	public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState) {
		super.onCreateView(inflater,container,savedInstanceState);
		View thisView = inflater.inflate(R.layout.frag_motion, container, false);
			
		if(tsOriginal == null)
			tsOriginal = BitmapFactory.decodeResource(getResources(), R.drawable.bgimage_turnswitch);
	    if(tsMatrix == null)
			tsMatrix = new Matrix();
	    
	    if(iv_dPad == null){
	    	iv_dPad = (ImageView) thisView.findViewById(R.id.iv_dpad);
	    	iv_dPad.setOnTouchListener(new RemoteOnTouchListener());
	    }
	    if(iv_turnSwitch == null){
		    iv_turnSwitch = (ImageView) thisView.findViewById(R.id.iv_turnswitch);
		    iv_turnSwitch.setOnTouchListener(new RemoteOnTouchListener());
		    iv_turnSwitch.getViewTreeObserver().addOnGlobalLayoutListener(new OnGlobalLayoutListener() {
		    	@Override
	            public void onGlobalLayout() {
	                if (tsHeight == 0 || tsWidth == 0) {
	                    tsHeight = iv_turnSwitch.getHeight();
	                    tsWidth = iv_turnSwitch.getWidth();
	                    Matrix resize = new Matrix();
	                    resize.postScale((float)Math.min(tsWidth, tsHeight) / (float)tsOriginal.getWidth(), (float)Math.min(tsWidth, tsHeight) / (float)tsOriginal.getHeight());
	                    tsScaled = Bitmap.createBitmap(tsOriginal, 0, 0, tsOriginal.getWidth(), tsOriginal.getHeight(), resize, false);
	                    float trnsX = tsWidth / 2 - tsScaled.getWidth() / 2;
	                    float trnsY = tsHeight / 2 - tsScaled.getHeight() / 2;
	                    tsMatrix.postTranslate(trnsX, trnsY);
	                    iv_turnSwitch.setImageBitmap(tsScaled);
	                    iv_turnSwitch.setImageMatrix(tsMatrix);
	                }
	            }
		    });
	    }
	    return thisView;
	}

	private class RemoteOnTouchListener implements OnTouchListener {
		private double startAngle, curAngle;
		private final int TURNSWITCH = R.id.iv_turnswitch;
		private final int DPAD 		 = R.id.iv_dpad;
		public boolean onTouch(View v, MotionEvent e) {
			final float X  = e.getX();
			final float Y  = e.getY();
			final int 	ID = v.getId();
			
			curAngle = getAngle(X, Y);
			
			switch (e.getAction()) {
				case MotionEvent.ACTION_MOVE:
					if(ID == TURNSWITCH){
						startAngle = rotateTurnSwitch(startAngle, curAngle);
					}else if(ID == DPAD){
						headForDirection(curAngle, X, Y);
					}
					break;
				case MotionEvent.ACTION_DOWN:
					startAngle = curAngle;
					break;
				case MotionEvent.ACTION_UP:
					if(ID == TURNSWITCH)
						resetTurnSwitch();
					send(MSG_TAG, poise);
		    }
	        return true;
	    }
	}

	private double getAngle(double xTouch, double yTouch) {
		final double X = xTouch - (tsWidth / 2d);
		final double Y = tsHeight - yTouch - (tsHeight / 2d);
		final double RAD = 180 / Math.PI;
		final double ASIN = Math.asin(Y / Math.hypot(X, Y));
		//Prevents Imageview-annihilation
		if(X == 0 & Y == 0)
			return 0;
		switch (X >= 0 ? (Y >= 0 ? 1 : 4) : (Y >= 0 ? 2 : 3)) { 
		//This number represents the quadrant in which the the current angle resides in.
		case 1:
			return ASIN * RAD;
		case 2:
			return 180 - ASIN * RAD;
		case 3:
			return 180 + (-1 * ASIN * RAD);
		case 4:
			return 360 + ASIN * RAD;
		default:
			return 0;
		}
	}

	private void resetTurnSwitch(){
		tsMatrix.reset();
        iv_turnSwitch.setImageMatrix(tsMatrix);
	}
	private double rotateTurnSwitch(double startAngle, double curAngle) {
		float angleDelta = (float)(startAngle - curAngle);
        tsMatrix.postRotate(angleDelta, tsWidth / 2, tsHeight / 2);
        iv_turnSwitch.setImageMatrix(tsMatrix);
        
        if(angleDelta != 0 & sensitivityTurnSwitch < Math.abs(angleDelta)){
			int rotation = angleDelta < 0 ? ANTICLOCK : CLOCK;
			int[] rot = new int[]{POISE,POISE,POISE,rotation,POISE};
			send(MSG_TAG, rot);
		}
        
        return curAngle;
    }
	
	private void headForDirection(double degrees, float xTouch, float yTouch){
		final int A,B;
		int DPAD_MID = 150;
		if(Math.abs(xTouch - DPAD_MID) < DPAD_MID * stillDpad &&
		   Math.abs(yTouch - DPAD_MID) < DPAD_MID * stillDpad){
			A = POISE;
			B = POISE;
		}else if(degrees < 22.5 | degrees >= 335){
			A = RIGHT;
			B = POISE;
		}else if(degrees < 67.5){
			A = RIGHT;
			B = FORWARD;
		}else if(degrees < 112.5){
			A = POISE;
			B = FORWARD;
		}else if(degrees < 157.5){
			A = LEFT;
			B = FORWARD;
		}else if(degrees < 202.5){
			A = LEFT;
			B = POISE;
		}else if(degrees < 247.5){
			A = LEFT;
			B = BACKWARD;
		}else if(degrees < 292.5){
			A = POISE;
			B = BACKWARD;
		}else if(degrees < 337.5){
			A = RIGHT;
			B = BACKWARD;
		}else{
			A = POISE;
			B = POISE;
		}
		int[] dir = new int[]{A,B,POISE,POISE,POISE};
		send(MSG_TAG, dir);
	}
}
