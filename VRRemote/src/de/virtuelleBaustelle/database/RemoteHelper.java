package de.virtuelleBaustelle.database;

import java.io.File;
import java.io.IOException;
import java.io.FileOutputStream;
import java.io.OutputStream;
import java.io.InputStream;

import android.content.Context;
import android.database.SQLException;
import android.database.sqlite.SQLiteDatabase;
import android.database.sqlite.SQLiteOpenHelper;
import android.util.Log;

public class RemoteHelper extends SQLiteOpenHelper {

	public static final String DB_PATH = "data/data/de.virtuelleBaustelle/databases/";
	public static final String DB_NAME = "remote.sqlite";
	
	public static final String TABLE_IP = "ip";
	public static final String COLUMN_CARTE_ID = "_id";
	public static final String COLUMN_DDN1 = "ddn1";
	public static final String COLUMN_DDN2 = "ddn2";
	public static final String COLUMN_DDN3 = "ddn3";
	public static final String COLUMN_DDN4 = "ddn4";
  
	private final Context context;
	private SQLiteDatabase mDataBase; 
	
	private static final int DATABASE_VERSION = 1;

	public RemoteHelper(Context context) throws IOException {
		super(context, RemoteDatabase.DATABASE_NAME, null, DATABASE_VERSION);
    	this.context = context;
		Log.d("DATABASE", "Database-Helper created!");
  	}
  
	@Override
	public void onCreate(SQLiteDatabase database) {
		try {
			createDataBase();
		} catch (IOException e) {
			Log.e("DATABASE", "IO-Exception while Database has been created!");
		}
		Log.d("DATABASE", "Database created!");
  	}

	@Override
	public void onUpgrade(SQLiteDatabase db, int oldVersion, int newVersion) {
		Log.w(RemoteHelper.class.getName(),
				"Upgrading database from version " + oldVersion + " to "
						+ newVersion + ", which will destroy all old data");
		db.execSQL("DROP TABLE IF EXISTS " + TABLE_IP);
		onCreate(db);

		Log.d("DATABASE", "Database updated!");
	}

  	public void createDataBase() throws IOException{
	    //If database not exists copy it from the assets
	
	    boolean mDataBaseExist = checkDataBase();
	    Log.d("DATABASE", "Does this db exists? " + mDataBaseExist);
	    if(!mDataBaseExist){
	    	this.getReadableDatabase();
	    	this.close();
	    	try {
	    		//Copy the database from assets
	    		copyDataBase();
	    		Log.e("DATABASE", "createDatabase database created");
	    	}catch (IOException e){
	    		throw new Error("ErrorCopyingDataBase");
	    	}
	    }
	}
  	
	//Copy the database from assets
	private void copyDataBase() throws IOException{
		InputStream databaseInput = context.getAssets().open(DB_NAME);
		String outFileName = DB_PATH + DB_NAME;
		OutputStream databaseOutput = new FileOutputStream(outFileName);
		byte[] mBuffer = new byte[1024];
		int length;
		while ((length = databaseInput.read(mBuffer))>0){
			databaseOutput.write(mBuffer, 0, length);
		}
		databaseOutput.flush();
		databaseOutput.close();
		databaseInput.close();
	}

	//Check that the database exists at: /data/data/de.virtuelleBaustelleSS13/databases/
	private boolean checkDataBase(){
		File dbFile = new File(DB_PATH + DB_NAME);
		return dbFile.exists();
	}

	//Open the database, so we can query it
	public boolean openDataBase() throws SQLException{
		String mPath = DB_PATH + DB_NAME;
		mDataBase = SQLiteDatabase.openDatabase(mPath, null, SQLiteDatabase.CREATE_IF_NECESSARY);
		return mDataBase != null;
	}

	@Override
	public synchronized void close() {
		if(mDataBase != null)
			mDataBase.close();
		super.close();
	}
} 
