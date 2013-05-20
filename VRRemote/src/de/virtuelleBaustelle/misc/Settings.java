package de.virtuelleBaustelle.misc;

public class Settings {
	private static String name = "";
	private static float stillDpad = 0.2f;
	private static double turnswitchInhibition = 2.0d;

	public static void setName(String n){
		name = n;
	}
	public static String getName(){
		return name;
	}
	
	public static float getSensitivityDpad() {
		return stillDpad;
	}
	public static void setStillDpad(float still) {
		stillDpad = still;
	}
	
	public static double getTurnswitchInhibition() {
		return turnswitchInhibition;
	}
	public static void setTurnswitchInhibition(double inhibition) {
		turnswitchInhibition = inhibition;
	}
}
