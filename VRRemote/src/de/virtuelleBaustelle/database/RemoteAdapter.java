package de.virtuelleBaustelle.database;

import java.io.IOException;
import android.content.Context;
import android.database.Cursor;
import android.database.SQLException;
import android.database.sqlite.SQLiteDatabase;
import android.util.Log;

public class RemoteAdapter{
	protected static final String TAG = "DataAdapter";
	private SQLiteDatabase database;
	private RemoteHelper helper;

	public RemoteAdapter(Context context){
		try {
			helper = new RemoteHelper(context);
		} catch (IOException e) {
			e.printStackTrace();
		}
	}

	public RemoteAdapter createDatabase() throws SQLException{
		try {
			helper.createDataBase();
		}catch (IOException e){
			Log.e(TAG, e.toString() + "  UnableToCreateDatabase");
			throw new Error("UnableToCreateDatabase");
		}
		return this;
	}

	public RemoteAdapter open() throws SQLException{
		try{
			helper.openDataBase();
			helper.close();
			database = helper.getReadableDatabase();
		}catch (SQLException e){
			Log.e(TAG, "open >>"+ e.toString());
			throw e;
		}
		return this;
    }

	public Cursor getData(String tableName){
		try{
			String sql ="SELECT * FROM " + tableName;

			Cursor mCur = database.rawQuery(sql, null);
			if (mCur!=null)
				mCur.moveToNext();
			return mCur;
		}catch (SQLException e){
			Log.e(TAG, "getTestData >>"+ e.toString());
			throw e;
		}
	}

	public void close(){
		helper.close();
	}
}
