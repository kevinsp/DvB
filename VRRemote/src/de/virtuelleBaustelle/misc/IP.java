package de.virtuelleBaustelle.misc;

public class IP {
	private int id;
	private int ddn1;
	private int ddn2;
	private int ddn3;
	private int ddn4;
	
	public IP(){}
	public IP(int id, int ddn1, int ddn2, int ddn3, int ddn4){
		this.id = id;
		this.ddn1 = ddn1;
		this.ddn2 = ddn2;
		this.ddn3 = ddn3;
		this.ddn4 = ddn4;
	}
	
	public void setID(int id){
		this.id = id;
	}
	public int getID(){
		return id;
	}
	
	public void setDDN(int num, int val){
		switch(num){
			case 1: this.ddn1 = val;
			case 2: this.ddn2 = val;
			case 3: this.ddn3 = val;
			case 4: this.ddn4 = val;
		}
	}
	public int getDDN(int num){
		switch(num){
			case  1: return ddn1;
			case  2: return ddn2;
			case  3: return ddn3;
			case  4: return ddn4;
			default: return -1;
		}
	}
	
	public String toString(){
		return ddn1 + "." + ddn2 + "." + ddn3 + "." + ddn4;
	}
}
