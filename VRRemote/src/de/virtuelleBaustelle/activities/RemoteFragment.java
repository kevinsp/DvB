package de.virtuelleBaustelle.activities;

import java.util.Arrays;

import org.json.JSONException;

import de.virtuelleBaustelle.misc.MissingConnectionException;
import android.app.Fragment;
import android.util.Log;

public abstract class RemoteFragment extends Fragment{
	
	protected int[] lastMessage;
	
	protected void send(String tag, int[] msg){
		if(!Arrays.equals(msg, lastMessage)){
			try {
				(MainActivity.class.cast(getActivity())).connection.sendJ(tag, msg);
				lastMessage = msg;
			} catch (JSONException e) {
				Log.e("Transmission", "Transmission failed!");
				e.printStackTrace();
			} catch (MissingConnectionException e1){
				Log.e("Connection", "Transmission failed: " + e1.getMessage());
				e1.printStackTrace();
			}
		}
	}
}