package de.virtuelleBaustelle.lists;

public class Waypoint {
	private String name;
	private int id;
	private int x;
	private int y;
	private int z;
	private float direction;
	private String description;
	
	public Waypoint(String name, int id, int x, int y, int z, float direction, String description){
		this.name 		 = name;
		this.x 			 = x;
		this.y 			 = y;
		this.z 			 = z;
		this.direction 	 = direction;
		this.description = description;
	}
	
	public String getName(){
		return name;
	}
	public int getID(){
		return id;
	}
	public int getX(){
		return x;
	}
	public int getY(){
		return y;
	}
	public int getZ(){
		return z;
	}
	public int[] getCoordinats(){
		return new int[]{x,y,z};
	}
	public float getDirection(){
		return direction;
	}
	public String getDescription(){
		return description;
	}
}
