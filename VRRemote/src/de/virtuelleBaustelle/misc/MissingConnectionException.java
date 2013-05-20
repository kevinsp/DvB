package de.virtuelleBaustelle.misc;

public class MissingConnectionException extends Exception {
	private static final long serialVersionUID = 1L;

	//Parameterless Constructor
      public MissingConnectionException() {
    	  super("This device is not connected to any Viz-Server");
      }

      //Constructor that accepts a message
      public MissingConnectionException(String message)
      {
         super(message);
      }
 }
