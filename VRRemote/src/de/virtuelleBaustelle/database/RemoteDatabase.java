package de.virtuelleBaustelle.database;

import java.util.ArrayList;
import java.util.List;

import de.virtuelleBaustelle.misc.IP;

import android.content.Context;
import android.database.Cursor;
import android.database.SQLException;

public class RemoteDatabase {

	// Database fields
	private RemoteAdapter adapter;
	public final static String DATABASE_NAME = "remote.sqlite";
	public RemoteDatabase(Context context) {
		//*/
		adapter = new RemoteAdapter(context);
		adapter.createDatabase();
	}
	
	public void open() throws SQLException {
		adapter.open();
	}

	public void close() {
		adapter.close();
	}

	public List<IP> getIPs() {
		List<IP> ips = new ArrayList<IP>();

		Cursor cursor = adapter.getData("ip");

		cursor.moveToFirst();
		while (!cursor.isAfterLast()) {
			IP ip = cursorToIP(cursor);
			ips.add(ip);
			cursor.moveToNext();
		}
		cursor.close();
		return ips;
	}

	private IP cursorToIP(Cursor cursor) {
		IP ip = new IP();
		ip.setID(cursor.getInt(0));
		ip.setDDN(1, cursor.getInt(1));
		ip.setDDN(2, cursor.getInt(2));
		ip.setDDN(3, cursor.getInt(3));
		ip.setDDN(4, cursor.getInt(4));
		return ip;
	}
} 
