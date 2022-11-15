$fn = 32;

module foot(inner = false, h=4) {
  difference() {
    if(!inner) {
      cylinder(d=8, h=h);
      if(h > 5) {
        cylinder(d=11, h=1.8);
        translate([0,0,1.5]) cylinder(d1=11, d2=8, h=1.8);
      } else {
        cylinder(d1=11, d2=8, h=1.8);
      }
    }
    translate([0,0,-0.01]) cylinder(r=1.2, h=h+1);
  }
}

refshiftx = 0.2;
refshifty = 4.5;

module feet(inner = false) {
  translate([-0.5+refshiftx,0+refshifty,0]) foot(inner);
  translate([67-4+refshiftx,0+refshifty,0]) foot(inner);
  translate([-0.5+refshiftx,70-4+refshifty,0]) foot(inner);
  translate([67-4+refshiftx,70-4+refshifty,0]) foot(inner);
}

feet();

module hold(r=2) {
  difference() {
    y = -6;
    union() {
      hull() {
        translate([0,y,0]) cylinder(r=5, h=4);
        translate([0,y+25,0]) cylinder(r=5, h=4);
      }
      hull() {
        translate([0,y+100,0]) cylinder(r=5, h=4);
        translate([0,y+95,0]) cylinder(r=5, h=4);
      }
    }
    translate([0,y,-0.01]) cylinder(r=r, h=5);
    translate([0,y+100,-0.01]) cylinder(r=r, h=5);
  }
}

difference() {
  play = 0.9;
  union() {
    translate([-5,0,0]) cube([166,90,1]);
    translate([80,0,0]) cube([81,90,2]);
    
    
    translate([-5,0,0]) cube([168,3,4]);
    translate([-5,86.5,0]) cube([115,3.5,4]);
    translate([-5,0,0]) cube([8,90,4]);
    translate([107,0,0]) cube([4,90,4]);
    translate([53,0,0]) cube([4,90,4]);
    
    translate([67-4+38.5-play,21-play,0]) foot(h=5.6);
    translate([67-4+38.5+55+play,21-play,0]) foot(h=5.6);
    translate([67-4+38.5-play,21+63+play,0]) foot(h=5.6);
    translate([67-4+38.5+55+play,21+63+play,0]) foot(h=5.6);
    
    translate([0,0,0]) hold();
    translate([100,0,0]) hold();
  }

  translate([67-4+38.5-play,21-play,0]) foot(true, h=5.6);
  translate([67-4+38.5+55+play,21-play,0]) foot(true, h=5.6);
  translate([67-4+38.5-play,21+63+play,0]) foot(true, h=5.6);
  translate([67-4+38.5+55+play,21+63+play,0]) foot(true, h=5.6);
  
  feet(inner = true);
  play2=0.5;
  translate([67-4+38.5-play2,21-play2,4.1]) cube([55+2*play2,63+2*play2,2]);
  
  translate([70,43,-1]) cube([30,25,5]);
  translate([120,-10,-1]) cube([50,27,10]);
  translate([33.5,70,-1]) cube([11,25,10]);
  translate([111,86,-1]) cube([40,25,10]);
}
    
*translate([56.5,0,0]) hold(1.2);
*translate([156.5,0,0]) hold(1.2);