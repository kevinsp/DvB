package de.virtuelleBaustelle.lists;

import java.util.ArrayList;
import java.util.List;

import de.virtuelleBaustelle.R;

import android.content.Context;
import android.view.LayoutInflater;
import android.view.View;
import android.view.View.OnClickListener;
import android.view.ViewGroup;
import android.widget.BaseAdapter;
import android.widget.Button;
import android.widget.TextView;

public class WaypointListAdapter extends BaseAdapter{
	private List<Waypoint> waypointData;
	private final LayoutInflater layoutInflater;
	
	public WaypointListAdapter(Context context, List<Waypoint> waypointData){
		this.waypointData = waypointData;
		layoutInflater = (LayoutInflater) context.getSystemService(Context.LAYOUT_INFLATER_SERVICE);
	}
	
	public WaypointListAdapter(Context context){
		waypointData = new ArrayList<Waypoint>();
		layoutInflater = (LayoutInflater) context.getSystemService(Context.LAYOUT_INFLATER_SERVICE);
	}
	
	@Override
	public int getCount() {
		return waypointData.size();
	}

	@Override
	public Object getItem(int position) {
		return waypointData.get(position);
	}

	@Override
	public long getItemId(int position) {
		return waypointData.get(position).getID();
	}

	@Override
	public View getView(final int position, View convertView, ViewGroup parent) {
		if (convertView == null) {
            convertView = layoutInflater.inflate(R.layout.listelement_waypoint, null);
		}
		int[] c = ((Waypoint)getItem(position)).getCoordinats();
		String coord = "[" + c[0] + "," + c[1] + "," + c[2] + "]";
		((TextView) convertView.findViewById(R.id.tv_wpname 		)).setText(((Waypoint)getItem(position)).getName());
    	((TextView) convertView.findViewById(R.id.tv_wpcoordination	)).setText(coord);
		((TextView) convertView.findViewById(R.id.tv_wpdescription	)).setText(((Waypoint)getItem(position)).getDescription());
    
		Button load = (Button) convertView.findViewById(R.id.b_wpload);
		Button delete = (Button) convertView.findViewById(R.id.b_wpdelete);
		OnClickListener listener = new OnClickListener(){
			@Override
			public void onClick(View v) {
				switch(v.getId()){
				case R.id.b_wpdelete:
					waypointData.remove(position);
					notifyDataSetChanged();
					
					break;
				case R.id.b_wpload:
					System.out.println("LOAD");
					break;
				}
			}
		};
		load.setOnClickListener(listener);
		delete.setOnClickListener(listener);
		
    	return convertView;
	}
	
	public void add(Waypoint w){
		waypointData.add(w);
	}
	
	public void remove(int position){
		waypointData.remove(position);
	}
	
	public void flush(){
		waypointData.clear();
	}
}
