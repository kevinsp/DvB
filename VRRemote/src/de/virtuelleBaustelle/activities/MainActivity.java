package de.virtuelleBaustelle.activities;

import java.util.List;

import de.virtuelleBaustelle.database.RemoteDatabase;
import de.virtuelleBaustelle.misc.Connector;
import de.virtuelleBaustelle.misc.IP;
import de.virtuelleBaustelle.R;

import android.os.Bundle;
import android.os.PowerManager;
import android.os.PowerManager.WakeLock;
import android.widget.*;
import android.util.Log;
import android.view.View;
import android.view.View.OnClickListener;
import android.app.*;
import android.content.Context;

public class MainActivity extends Activity implements OnClickListener {
	private ImageButton ib_navigation, ib_waypoint, ib_settings, ib_help;
	
	private final String IP_DIAG_TITLE = "Bitte Ip-Adresse eingeben!";
	private Dialog dialogIP;
	Connector connection;
	
	private WakeLock wakeLock;
	
	private final String	motionTag = "MOTION";
	private final String	waypointTag = "WAYPOINT";
	private final Fragment 	fragmentMotion = new MotionFragment();
	private final Fragment 	fragmentWaypoint = new WaypointFragment();
	
	private RemoteDatabase database;
	
	@Override
	public void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.activity_controller);
		
		prepareEnvironment();
		prepareDatabase();
		prepareNavigationBar();
		connect();
		
		//Sets the initial fragment
		switchFragment(fragmentMotion, motionTag);
	}
	
	//Is used to define system-relevant behaviour, such as wakelock (prevents screenlock)
	@SuppressWarnings("deprecation")
	private void prepareEnvironment(){
		PowerManager pm = (PowerManager) getSystemService(Context.POWER_SERVICE);
		this.wakeLock = pm.newWakeLock(PowerManager.SCREEN_DIM_WAKE_LOCK, "WakeLock");
		wakeLock.acquire();
	}

	private void prepareDatabase(){
		database = new RemoteDatabase(this);
	}
	
	private void prepareNavigationBar(){
		(ib_navigation  = (ImageButton) findViewById(R.id.ib_movement)).setOnClickListener(this);
		(ib_waypoint	= (ImageButton) findViewById(R.id.ib_waypoint)).setOnClickListener(this);
		(ib_settings	= (ImageButton) findViewById(R.id.ib_settings)).setOnClickListener(this);
		(ib_help		= (ImageButton) findViewById(R.id.ib_help)).setOnClickListener(this);
	}

	//Creates a dialog, which asks for the server's ip and defines the connection
	private void connect(){
		dialogIP = new Dialog(this);
		dialogIP.setTitle(IP_DIAG_TITLE);
		dialogIP.setContentView(R.layout.dialog_ip);
		dialogIP.setCanceledOnTouchOutside(false);
		
		final Button ok = (Button) dialogIP.findViewById(R.id.b_ok);
		ok.setOnClickListener(new OnClickListener() {
			@Override
			public void onClick(View v) {
				database.open();
				List<IP> ipList = database.getIPs();
				database.close();
				
				int count = ipList.isEmpty() ? 0 : ipList.size();
				Log.d("IP-LISTE", "Es sind " + count + " IPs gespeichert!");
				String ddn1 = ((EditText) dialogIP.findViewById(R.id.et_ip1)).getText().toString();
				String ddn2 = ((EditText) dialogIP.findViewById(R.id.et_ip2)).getText().toString();
				String ddn3 = ((EditText) dialogIP.findViewById(R.id.et_ip3)).getText().toString();
				String ddn4 = ((EditText) dialogIP.findViewById(R.id.et_ip4)).getText().toString();
				if(!(ddn1.isEmpty() | ddn2.isEmpty() | ddn3.isEmpty() | ddn4.isEmpty())){
					IP ip = new IP(0, Integer.valueOf(ddn1),
									  Integer.valueOf(ddn2),
									  Integer.valueOf(ddn3),
									  Integer.valueOf(ddn4));
					connection = new Connector(ip.toString());
					dialogIP.dismiss();
					
					Log.d("Connection", "Connection established (" + ip + ")");
					}
			}
		});
		dialogIP.show();
	}

	//Generally switches the visible Fragment.
	//This method may not be modified
	private void switchFragment(Fragment f, String TAG){
		FragmentTransaction ft = getFragmentManager().beginTransaction();
		(ft.replace(R.id.ll_fragment, f, TAG)).commit();
		ft.setTransition(FragmentTransaction.TRANSIT_NONE);
		Log.d("FragmentTransaction", "Fragment switched to : " + TAG);
	}

	public void onClick(View v) {
		if(v == ib_navigation & !fragmentMotion.isVisible()){
			switchFragment(fragmentMotion, motionTag);
		}else if(v == ib_waypoint & !fragmentWaypoint.isVisible()){
			switchFragment(fragmentWaypoint, waypointTag);
		}else if(v == ib_settings){
			//switchFragment(new SettingsFragment(), "SETTINGS");
		}else if(v == ib_help){
			//switchFragment(new HelpFragment(), "HELP");
		}
	}

	//Closes the Remote-Connection and releases system-ressources, such as wakelock
	//OnDestroy() is called to foreclose the system to become too comsumptive of eletric current
	public void onStop(){
		super.onStop();
		wakeLock.release();
		connection.closeStreams();
		onDestroy();
	}
}