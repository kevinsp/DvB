package de.virtuelleBaustelle.activities;

import de.virtuelleBaustelle.lists.Waypoint;
import de.virtuelleBaustelle.lists.WaypointListAdapter;
import de.virtuelleBaustelle.R;

import android.app.*;
import android.os.Bundle;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.View.OnClickListener;
import android.view.ViewGroup;
import android.widget.*;

public class WaypointFragment extends Fragment{
	
	private WaypointListAdapter wladapter;
	private Button addWaypoint;
	private ListView waypoints;
	
	private final String WAYPOINT_DIAG_TITLE = "Bitte Wegpunkt-Name eingeben.";
	private Dialog dialogNewWaypoint;
	
	public View onCreateView(LayoutInflater inflater, 
			ViewGroup container, Bundle savedInstanceState) {
		super.onCreateView(inflater,container,savedInstanceState);
		
		View thisView = inflater.inflate(R.layout.frag_waypoint, container, false);
		if(waypoints == null){
			waypoints = (ListView) thisView.findViewById(R.id.lv_waypoints);
		}

		if(wladapter == null){
			wladapter = new WaypointListAdapter(thisView.getContext());
			waypoints.setAdapter(wladapter);
		}

		addWaypoint = (Button) thisView.findViewById(R.id.b_newwaypoint);
		addWaypoint.setOnClickListener(new WaypointOnClickListener());

		return thisView;
	}
	
	class WaypointOnClickListener implements OnClickListener{
		public void onClick(View v){
			switch(v.getId()){
				case R.id.b_newwaypoint:
					dialogNewWaypoint = new Dialog(getActivity());
					dialogNewWaypoint.setTitle(WAYPOINT_DIAG_TITLE);
					dialogNewWaypoint.setContentView(R.layout.dialog_newwaypoint);
					dialogNewWaypoint.setCanceledOnTouchOutside(false);
					
					final Button OK = (Button) dialogNewWaypoint
							.findViewById(R.id.b_wp_ok);
					OK.setOnClickListener(this);
					
					final Button ABORT = (Button) dialogNewWaypoint
							.findViewById(R.id.b_wp_abort);
					ABORT.setOnClickListener(this);
					
					dialogNewWaypoint.show();
					break;
				case R.id.b_wp_ok:
					if(dialogNewWaypoint != null){
						final String NAME = ((EditText) dialogNewWaypoint
								.findViewById(R.id.et_waypointname))
								.getText().toString();
						
						if(!NAME.isEmpty()){
							Waypoint w = new Waypoint(NAME, 0, 0, 0, 0, 0, "Test");
							wladapter.add(w);
							wladapter.notifyDataSetChanged();
							dialogNewWaypoint.dismiss();
						}else{
							Log.e("Waypoint", "No Waypoint-Dialog is shown!");
						}
					}
					break;
				case R.id.b_wp_abort:
					dialogNewWaypoint.dismiss();
					break;
			}
		}
	}
}
