package de.virtuelleBaustelle.misc;

import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.IOException;
import java.io.PrintWriter;
import java.net.Socket;
import java.util.Iterator;

import org.json.JSONException;
import org.json.JSONObject;
import org.json.JSONStringer;

import android.os.AsyncTask;
import android.util.Log;

public class Connector extends AsyncTask<String, Void, Void>{
	JSONStringer jstringer;
	PrintWriter pw;
	DataInputStream is;
	DataOutputStream os;
	
	private final String IP;
	private final int PORT = 57891;
	private Socket sock = null;

	public Connector(String ip){
		IP = ip;
		execute(ip);
	}
	
	public void sendJ(String name, int[] valArr) throws JSONException, MissingConnectionException
	{
		JSONObject jsend = fillJson(name, valArr);
	    send(jsend);
	}

	public void sendJEnd() throws JSONException, MissingConnectionException
	{
		JSONObject jsend = new JSONObject();
		jsend.put("end", 1);
		send(jsend);
	}

	private void send(JSONObject obj) throws JSONException, MissingConnectionException{
		if(pw == null)
			throw new MissingConnectionException();
		jstringer = new JSONStringer();
		jstringer = makePackage(obj, jstringer);
		pw.println(jstringer);
		pw.flush();
	}
	
	public JSONObject fillJson(String name, int[] valArr) throws JSONException
	{
		JSONObject all = new JSONObject();
		JSONObject values = new JSONObject();
		JSONObject move = new JSONObject();
		JSONObject rot = new JSONObject();

		move.put("a", valArr[0]);
		move.put("b", valArr[1]);

		rot.put("x", valArr[2]);
		rot.put("y", valArr[3]);

		values.put("m", move);
		values.put("r", rot);
		values.put("e", valArr[4]);
		
		all.put(name, values);

		return all;
	}

	public JSONStringer makePackage(JSONObject jsend, JSONStringer jstringer) throws JSONException{
		if (jsend != null){
			@SuppressWarnings("unchecked") // Using legacy API
			Iterator<String> itKeys = jsend.keys();
	        if(itKeys.hasNext())
	        	jstringer.object();
	        while (itKeys.hasNext()){
	            String k = itKeys.next();
	            jstringer.key(k).value(jsend.get(k));
	        }         
	    }
		jstringer.endObject();
		
		return jstringer;
	}

	public void closeStreams(){
		try{
			if (is != null)
				is.close();
			if (os != null)
				os.close();
		}catch (IOException e){
			Log.e("Connection", "An IO-Exception occured, while the Socket-Streams should have been closed;!");
		}
	}
	
	@Override
	protected Void doInBackground(String... params){
		try {
			sock = new Socket(IP, PORT);
			is = new DataInputStream(sock.getInputStream());
			os = new DataOutputStream(sock.getOutputStream());
			pw = new PrintWriter(os);
			Log.d("Connection", "Connection established : " + IP);
		} catch (IOException e) {
			e.printStackTrace();
		}
		
		return null;
	}
}
