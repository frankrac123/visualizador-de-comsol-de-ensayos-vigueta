/*
 * vigueta_fractura.java
 */

import com.comsol.model.*;
import com.comsol.model.util.*;

/** Model exported on Oct 10 2026, 12:10 by COMSOL 6.1.0.282. */
public class vigueta_fractura {

  public static Model run() {
    Model model = ModelUtil.create("Model");

    model
         .modelPath(".");

    model.label("vigueta_fractura.mph");

    model.param().set("Emat", "25000[MPa]");
    model.param().set("numat", "0.2");
    model.param().set("ftmat", "0.87851483[MPa]");
    model.param().set("Gfmat", "220[J/m^2]");
    model.param().set("Kcoh", "100000000000000.0[N/m^3]");
    model.param().set("bmat", "130.3333333333333[mm]");
    model.param().set("dload", "0.003[mm]");
    model.param().set("cmod", "5e-07[mm]");

    model.component().create("comp1", true);

    model.component("comp1").geom().create("geom1", 2);

    model.component("comp1").sorder("quadratic");

    model.component("comp1").mesh().create("mesh1");

    model.component("comp1").geom("geom1").lengthUnit("mm");
    model.component("comp1").geom("geom1").create("L", "Polygon");
    model.component("comp1").geom("geom1").feature("L").set("selresult", true);
    model.component("comp1").geom("geom1").feature("L").set("selresultshow", "all");
    model.component("comp1").geom("geom1").feature("L")
         .set("x", new int[]{-251, -228, -225, -222, 0, 0, -72, -75, -78, -251});
    model.component("comp1").geom("geom1").feature("L").set("y", new int[]{0, 0, 0, 0, 0, 151, 151, 151, 151, 151});
    model.component("comp1").geom("geom1").create("R", "Polygon");
    model.component("comp1").geom("geom1").feature("R").set("selresult", true);
    model.component("comp1").geom("geom1").feature("R").set("selresultshow", "all");
    model.component("comp1").geom("geom1").feature("R")
         .set("x", new int[]{0, 222, 225, 228, 251, 251, 78, 75, 72, 0});
    model.component("comp1").geom("geom1").feature("R").set("y", new int[]{0, 0, 0, 0, 0, 151, 151, 151, 151, 151});
    model.component("comp1").geom("geom1").create("bl", "Circle");
    model.component("comp1").geom("geom1").feature("bl").set("selresult", true);
    model.component("comp1").geom("geom1").feature("bl").set("selresultshow", "all");
    model.component("comp1").geom("geom1").feature("bl").set("pos", new int[]{-225, -15});
    model.component("comp1").geom("geom1").feature("bl").set("r", 15);
    model.component("comp1").geom("geom1").create("br", "Circle");
    model.component("comp1").geom("geom1").feature("br").set("selresult", true);
    model.component("comp1").geom("geom1").feature("br").set("selresultshow", "all");
    model.component("comp1").geom("geom1").feature("br").set("pos", new int[]{225, -15});
    model.component("comp1").geom("geom1").feature("br").set("r", 15);
    model.component("comp1").geom("geom1").create("tl", "Circle");
    model.component("comp1").geom("geom1").feature("tl").set("selresult", true);
    model.component("comp1").geom("geom1").feature("tl").set("selresultshow", "all");
    model.component("comp1").geom("geom1").feature("tl").set("pos", new int[]{-75, 166});
    model.component("comp1").geom("geom1").feature("tl").set("r", 15);
    model.component("comp1").geom("geom1").create("tr", "Circle");
    model.component("comp1").geom("geom1").feature("tr").set("selresult", true);
    model.component("comp1").geom("geom1").feature("tr").set("selresultshow", "all");
    model.component("comp1").geom("geom1").feature("tr").set("pos", new int[]{75, 166});
    model.component("comp1").geom("geom1").feature("tr").set("r", 15);
    model.component("comp1").geom("geom1").feature("fin").label("Formar ensamble");
    model.component("comp1").geom("geom1").feature("fin").set("action", "assembly");
    model.component("comp1").geom("geom1").feature("fin").set("createpairs", false);
    model.component("comp1").geom("geom1").run();

    model.component("comp1").selection().create("cohLbox", "Box");
    model.component("comp1").selection("cohLbox").set("entitydim", 1);
    model.component("comp1").selection().create("cohL", "Explicit");
    model.component("comp1").selection("cohL").geom("geom1", 1);
    model.component("comp1").selection("cohL").set(10);
    model.component("comp1").selection().create("cohRbox", "Box");
    model.component("comp1").selection("cohRbox").set("entitydim", 1);
    model.component("comp1").selection().create("cohR", "Explicit");
    model.component("comp1").selection("cohR").geom("geom1", 1);
    model.component("comp1").selection("cohR").set(19);
    model.component("comp1").selection().create("dst_blbox", "Box");
    model.component("comp1").selection("dst_blbox").set("entitydim", 1);
    model.component("comp1").selection().create("dst_bl", "Explicit");
    model.component("comp1").selection("dst_bl").geom("geom1", 1);
    model.component("comp1").selection("dst_bl").set(4, 5);
    model.component("comp1").selection().create("dst_brbox", "Box");
    model.component("comp1").selection("dst_brbox").set("entitydim", 1);
    model.component("comp1").selection().create("dst_br", "Explicit");
    model.component("comp1").selection("dst_br").geom("geom1", 1);
    model.component("comp1").selection("dst_br").set(25, 26);
    model.component("comp1").selection().create("dst_tlbox", "Box");
    model.component("comp1").selection("dst_tlbox").set("entitydim", 1);
    model.component("comp1").selection().create("dst_tl", "Explicit");
    model.component("comp1").selection("dst_tl").geom("geom1", 1);
    model.component("comp1").selection("dst_tl").set(7, 8);
    model.component("comp1").selection().create("dst_trbox", "Box");
    model.component("comp1").selection("dst_trbox").set("entitydim", 1);
    model.component("comp1").selection().create("dst_tr", "Explicit");
    model.component("comp1").selection("dst_tr").geom("geom1", 1);
    model.component("comp1").selection("dst_tr").set(22, 23);
    model.component("comp1").selection().create("pinbox", "Box");
    model.component("comp1").selection("pinbox").set("entitydim", 0);
    model.component("comp1").selection().create("pin", "Explicit");
    model.component("comp1").selection("pin").geom("geom1", 0);
    model.component("comp1").selection("pin").set(4);
    model.component("comp1").selection().create("cLbox", "Box");
    model.component("comp1").selection("cLbox").set("entitydim", 0);
    model.component("comp1").selection().create("cL", "Explicit");
    model.component("comp1").selection("cL").geom("geom1", 0);
    model.component("comp1").selection("cL").set(9);
    model.component("comp1").selection().create("cRbox", "Box");
    model.component("comp1").selection("cRbox").set("entitydim", 0);
    model.component("comp1").selection().create("cR", "Explicit");
    model.component("comp1").selection("cR").geom("geom1", 0);
    model.component("comp1").selection("cR").set(19);
    model.component("comp1").selection().create("gRbox", "Box");
    model.component("comp1").selection("gRbox").set("entitydim", 0);
    model.component("comp1").selection().create("gR", "Explicit");
    model.component("comp1").selection("gR").geom("geom1", 0);
    model.component("comp1").selection("gR").set(25);
    model.component("comp1").selection("cohLbox").set("xmin", "-0.001[mm]");
    model.component("comp1").selection("cohLbox").set("xmax", "0.001[mm]");
    model.component("comp1").selection("cohLbox").set("ymin", "-0.001[mm]");
    model.component("comp1").selection("cohLbox").set("ymax", "151.001[mm]");
    model.component("comp1").selection("cohLbox").set("condition", "inside");
    model.component("comp1").selection("cohRbox").set("xmin", "-0.001[mm]");
    model.component("comp1").selection("cohRbox").set("xmax", "0.001[mm]");
    model.component("comp1").selection("cohRbox").set("ymin", "-0.001[mm]");
    model.component("comp1").selection("cohRbox").set("ymax", "151.001[mm]");
    model.component("comp1").selection("cohRbox").set("condition", "inside");
    model.component("comp1").selection("dst_blbox").set("xmin", "-228.001[mm]");
    model.component("comp1").selection("dst_blbox").set("xmax", "-221.999[mm]");
    model.component("comp1").selection("dst_blbox").set("ymin", "-0.001[mm]");
    model.component("comp1").selection("dst_blbox").set("ymax", "0.001[mm]");
    model.component("comp1").selection("dst_blbox").set("condition", "inside");
    model.component("comp1").selection("dst_brbox").set("xmin", "221.999[mm]");
    model.component("comp1").selection("dst_brbox").set("xmax", "228.001[mm]");
    model.component("comp1").selection("dst_brbox").set("ymin", "-0.001[mm]");
    model.component("comp1").selection("dst_brbox").set("ymax", "0.001[mm]");
    model.component("comp1").selection("dst_brbox").set("condition", "inside");
    model.component("comp1").selection("dst_tlbox").set("xmin", "-78.001[mm]");
    model.component("comp1").selection("dst_tlbox").set("xmax", "-71.999[mm]");
    model.component("comp1").selection("dst_tlbox").set("ymin", "150.999[mm]");
    model.component("comp1").selection("dst_tlbox").set("ymax", "151.001[mm]");
    model.component("comp1").selection("dst_tlbox").set("condition", "inside");
    model.component("comp1").selection("dst_trbox").set("xmin", "71.999[mm]");
    model.component("comp1").selection("dst_trbox").set("xmax", "78.001[mm]");
    model.component("comp1").selection("dst_trbox").set("ymin", "150.999[mm]");
    model.component("comp1").selection("dst_trbox").set("ymax", "151.001[mm]");
    model.component("comp1").selection("dst_trbox").set("condition", "inside");
    model.component("comp1").selection("pinbox").set("xmin", "-225.001[mm]");
    model.component("comp1").selection("pinbox").set("xmax", "-224.999[mm]");
    model.component("comp1").selection("pinbox").set("ymin", "-0.001[mm]");
    model.component("comp1").selection("pinbox").set("ymax", "0.001[mm]");
    model.component("comp1").selection("pinbox").set("condition", "inside");
    model.component("comp1").selection("cLbox").set("xmin", "-0.001[mm]");
    model.component("comp1").selection("cLbox").set("xmax", "0.001[mm]");
    model.component("comp1").selection("cLbox").set("ymin", "-0.001[mm]");
    model.component("comp1").selection("cLbox").set("ymax", "0.001[mm]");
    model.component("comp1").selection("cLbox").set("condition", "inside");
    model.component("comp1").selection("cRbox").set("xmin", "-0.001[mm]");
    model.component("comp1").selection("cRbox").set("xmax", "0.001[mm]");
    model.component("comp1").selection("cRbox").set("ymin", "-0.001[mm]");
    model.component("comp1").selection("cRbox").set("ymax", "0.001[mm]");
    model.component("comp1").selection("cRbox").set("condition", "inside");
    model.component("comp1").selection("gRbox").set("xmin", "224.999[mm]");
    model.component("comp1").selection("gRbox").set("xmax", "225.001[mm]");
    model.component("comp1").selection("gRbox").set("ymin", "-0.001[mm]");
    model.component("comp1").selection("gRbox").set("ymax", "0.001[mm]");
    model.component("comp1").selection("gRbox").set("condition", "inside");

    model.component("comp1").pair().create("coh", "Contact");
    model.component("comp1").pair("coh").source().named("cohL");
    model.component("comp1").pair("coh").destination().named("cohR");
    model.component("comp1").pair().create("cp_bl", "Contact");
    model.component("comp1").pair("cp_bl").source().named("geom1_bl_bnd");
    model.component("comp1").pair("cp_bl").destination().named("dst_bl");
    model.component("comp1").pair().create("cp_br", "Contact");
    model.component("comp1").pair("cp_br").source().named("geom1_br_bnd");
    model.component("comp1").pair("cp_br").destination().named("dst_br");
    model.component("comp1").pair().create("cp_tl", "Contact");
    model.component("comp1").pair("cp_tl").source().named("geom1_tl_bnd");
    model.component("comp1").pair("cp_tl").destination().named("dst_tl");
    model.component("comp1").pair().create("cp_tr", "Contact");
    model.component("comp1").pair("cp_tr").source().named("geom1_tr_bnd");
    model.component("comp1").pair("cp_tr").destination().named("dst_tr");

    model.component("comp1").material().create("mat1", "Common");
    model.component("comp1").material("mat1").selection().set(1, 4);

    model.component("comp1").cpl().create("ptcL", "Integration");
    model.component("comp1").cpl().create("ptcR", "Integration");
    model.component("comp1").cpl().create("ptgR", "Integration");
    model.component("comp1").cpl().create("ptPin", "Integration");
    model.component("comp1").cpl("ptcL").selection().named("cL");
    model.component("comp1").cpl("ptcR").selection().named("cR");
    model.component("comp1").cpl("ptgR").selection().named("gR");
    model.component("comp1").cpl("ptPin").selection().named("pin");

    model.component("comp1").physics().create("solid", "SolidMechanics", "geom1");
    model.component("comp1").physics("solid").create("cntC", "SolidContact", 1);
    model.component("comp1").physics("solid").feature("cntC").create("adh1", "Adhesion", 1);
    model.component("comp1").physics("solid").feature("cntC").create("dco1", "Decohesion", 1);
    model.component("comp1").physics("solid").create("rd1", "RigidDomain", 2);
    model.component("comp1").physics("solid").feature("rd1").selection().named("geom1_bl_dom");
    model.component("comp1").physics("solid").feature("rd1").create("pdr1", "PrescribedDispRot", -1);
    model.component("comp1").physics("solid").feature("rd1").feature("pdr1")
         .set("RotationType", "PrescribedRotationGroup");
    model.component("comp1").physics("solid").create("cnt1", "SolidContact", 1);
    model.component("comp1").physics("solid").create("rd2", "RigidDomain", 2);
    model.component("comp1").physics("solid").feature("rd2").selection().named("geom1_br_dom");
    model.component("comp1").physics("solid").feature("rd2").create("pdr1", "PrescribedDispRot", -1);
    model.component("comp1").physics("solid").feature("rd2").feature("pdr1")
         .set("RotationType", "PrescribedRotationGroup");
    model.component("comp1").physics("solid").create("cnt2", "SolidContact", 1);
    model.component("comp1").physics("solid").create("rd3", "RigidDomain", 2);
    model.component("comp1").physics("solid").feature("rd3").selection().set(3, 5);
    model.component("comp1").physics("solid").feature("rd3").create("pdr1", "PrescribedDispRot", -1);
    model.component("comp1").physics("solid").create("cnt3", "SolidContact", 1);
    model.component("comp1").physics("solid").create("cnt4", "SolidContact", 1);
    model.component("comp1").physics("solid").create("pin1", "Displacement0", 0);
    model.component("comp1").physics("solid").feature("pin1").selection().named("pin");
    model.component("comp1").physics().create("ge", "GlobalEquations");

    model.component("comp1").mesh("mesh1").create("ft", "FreeTri");
    model.component("comp1").mesh("mesh1").feature("ft").selection().geom("geom1", 2);
    model.component("comp1").mesh("mesh1").feature("ft").selection().all();
    model.component("comp1").mesh("mesh1").feature("ft").create("contact", "Size");
    model.component("comp1").mesh("mesh1").feature("ft").create("roller", "Size");
    model.component("comp1").mesh("mesh1").feature("ft").create("fracture", "Size");
    model.component("comp1").mesh("mesh1").feature("ft").feature("contact").selection().geom("geom1", 1);
    model.component("comp1").mesh("mesh1").feature("ft").feature("contact").selection()
         .set(4, 5, 7, 8, 22, 23, 25, 26);
    model.component("comp1").mesh("mesh1").feature("ft").feature("roller").selection().geom("geom1", 1);
    model.component("comp1").mesh("mesh1").feature("ft").feature("roller").selection()
         .set(11, 12, 13, 14, 15, 16, 17, 18, 29, 30, 31, 32, 33, 34, 35, 36);
    model.component("comp1").mesh("mesh1").feature("ft").feature("fracture").selection().geom("geom1", 1);
    model.component("comp1").mesh("mesh1").feature("ft").feature("fracture").selection().set(10, 19);

    model.component("comp1").material("mat1").propertyGroup("def").set("youngsmodulus", "Emat");
    model.component("comp1").material("mat1").propertyGroup("def").set("poissonsratio", "numat");
    model.component("comp1").material("mat1").propertyGroup("def").set("density", "2331.488[kg/m^3]");

    model.component("comp1").cpl("ptcL").label("Integraci\u00f3n 2.1");
    model.component("comp1").cpl("ptcR").label("Integraci\u00f3n 3.1");
    model.component("comp1").cpl("ptgR").label("Integraci\u00f3n 4.1");
    model.component("comp1").cpl("ptPin").label("Integraci\u00f3n 5");

    model.component("comp1").physics("solid").prop("ShapeProperty").set("order_displacement", 1);
    model.component("comp1").physics("solid").prop("Type2D").set("Type2D", "PlaneStress");
    model.component("comp1").physics("solid").prop("d").set("d", "bmat");
    model.component("comp1").physics("solid").feature("cntC").set("penaltyCtrlPenalty", "userDefined");
    model.component("comp1").physics("solid").feature("cntC").set("pn_penalty", "Kcoh");
    model.component("comp1").physics("solid").feature("cntC").set("zeroInitGap", true);
    model.component("comp1").physics("solid").feature("cntC").set("automaticQuadrature", false);
    model.component("comp1").physics("solid").feature("cntC").set("integrationOrder", 2);
    model.component("comp1").physics("solid").feature("cntC").set("E_char", "Emat");
    model.component("comp1").physics("solid").feature("cntC").set("storeContactEnergy", true);
    model.component("comp1").physics("solid").feature("cntC").set("pairs", "coh");
    model.component("comp1").physics("solid").feature("cntC").feature("adh1").set("ActivationCriterion", "Always");
    model.component("comp1").physics("solid").feature("cntC").feature("adh1").set("ntau", 1);
    model.component("comp1").physics("solid").feature("cntC").feature("dco1").set("storeDmgEnergy", true);
    model.component("comp1").physics("solid").feature("cntC").feature("dco1").set("sigmat", "ftmat");
    model.component("comp1").physics("solid").feature("cntC").feature("dco1").set("sigmas", "ftmat");
    model.component("comp1").physics("solid").feature("cntC").feature("dco1").set("Gct", "Gfmat");
    model.component("comp1").physics("solid").feature("cntC").feature("dco1").set("Gcs", "Gfmat");
    model.component("comp1").physics("solid").feature("rd1").set("rho_mat", "userdef");
    model.component("comp1").physics("solid").feature("rd1").set("rho", "7850[kg/m^3]");
    model.component("comp1").physics("solid").feature("rd1").feature("pdr1")
         .set("Direction", new int[][]{{1}, {1}, {0}});
    model.component("comp1").physics("solid").feature("rd1").feature("pdr1").set("UnidirectionalConstraints", true);
    model.component("comp1").physics("solid").feature("cnt1").set("penaltyCtrlPenalty", "ManualTuning");
    model.component("comp1").physics("solid").feature("cnt1").set("fp_penalty", 10);
    model.component("comp1").physics("solid").feature("cnt1").set("automaticQuadrature", false);
    model.component("comp1").physics("solid").feature("cnt1").set("integrationOrder", 2);
    model.component("comp1").physics("solid").feature("cnt1").set("E_char", "Emat");
    model.component("comp1").physics("solid").feature("cnt1").set("storeContactEnergy", true);
    model.component("comp1").physics("solid").feature("cnt1").set("pairs", "cp_bl");
    model.component("comp1").physics("solid").feature("rd2").set("rho_mat", "userdef");
    model.component("comp1").physics("solid").feature("rd2").set("rho", "7850[kg/m^3]");
    model.component("comp1").physics("solid").feature("rd2").feature("pdr1")
         .set("Direction", new int[][]{{1}, {1}, {0}});
    model.component("comp1").physics("solid").feature("rd2").feature("pdr1").set("UnidirectionalConstraints", true);
    model.component("comp1").physics("solid").feature("cnt2").set("penaltyCtrlPenalty", "ManualTuning");
    model.component("comp1").physics("solid").feature("cnt2").set("fp_penalty", 10);
    model.component("comp1").physics("solid").feature("cnt2").set("automaticQuadrature", false);
    model.component("comp1").physics("solid").feature("cnt2").set("integrationOrder", 2);
    model.component("comp1").physics("solid").feature("cnt2").set("E_char", "Emat");
    model.component("comp1").physics("solid").feature("cnt2").set("storeContactEnergy", true);
    model.component("comp1").physics("solid").feature("cnt2").set("pairs", "cp_br");
    model.component("comp1").physics("solid").feature("rd3").set("rho_mat", "userdef");
    model.component("comp1").physics("solid").feature("rd3").set("rho", "7850[kg/m^3]");
    model.component("comp1").physics("solid").feature("rd3").feature("pdr1")
         .set("Direction", new int[][]{{1}, {1}, {0}});
    model.component("comp1").physics("solid").feature("rd3").feature("pdr1")
         .set("U0", new String[][]{{"0"}, {"-qact*1[mm]"}, {"0"}});
    model.component("comp1").physics("solid").feature("rd3").feature("pdr1").set("UnidirectionalConstraints", true);
    model.component("comp1").physics("solid").feature("cnt3").set("penaltyCtrlPenalty", "ManualTuning");
    model.component("comp1").physics("solid").feature("cnt3").set("fp_penalty", 10);
    model.component("comp1").physics("solid").feature("cnt3").set("automaticQuadrature", false);
    model.component("comp1").physics("solid").feature("cnt3").set("integrationOrder", 2);
    model.component("comp1").physics("solid").feature("cnt3").set("E_char", "Emat");
    model.component("comp1").physics("solid").feature("cnt3").set("storeContactEnergy", true);
    model.component("comp1").physics("solid").feature("cnt3").set("pairs", "cp_tl");
    model.component("comp1").physics("solid").feature("cnt4").set("penaltyCtrlPenalty", "ManualTuning");
    model.component("comp1").physics("solid").feature("cnt4").set("fp_penalty", 10);
    model.component("comp1").physics("solid").feature("cnt4").set("automaticQuadrature", false);
    model.component("comp1").physics("solid").feature("cnt4").set("integrationOrder", 2);
    model.component("comp1").physics("solid").feature("cnt4").set("E_char", "Emat");
    model.component("comp1").physics("solid").feature("cnt4").set("storeContactEnergy", true);
    model.component("comp1").physics("solid").feature("cnt4").set("pairs", "cp_tr");
    model.component("comp1").physics("solid").feature("pin1").set("Direction", new int[][]{{1}, {0}, {0}});
    model.component("comp1").physics("ge").feature("ge1").set("name", "qact");
    model.component("comp1").physics("ge").feature("ge1").set("equation", "(ptcR(u)-ptcL(u)-cmod)/1[mm]");
    model.component("comp1").physics("ge").feature("ge1").set("initialValueU", 0.003);
    model.component("comp1").physics("ge").feature("ge1")
         .set("description", "Head displacement; physical bottom opening controller");

    model.component("comp1").mesh("mesh1").feature("size").set("custom", "on");
    model.component("comp1").mesh("mesh1").feature("size").set("hmax", "8.0[mm]");
    model.component("comp1").mesh("mesh1").feature("size").set("hmin", ".025[mm]");
    model.component("comp1").mesh("mesh1").feature("size").set("hgrad", 1.4);
    model.component("comp1").mesh("mesh1").feature("ft").feature("contact").set("custom", "on");
    model.component("comp1").mesh("mesh1").feature("ft").feature("contact").set("hmax", "0.04[mm]");
    model.component("comp1").mesh("mesh1").feature("ft").feature("contact").set("hmaxactive", true);
    model.component("comp1").mesh("mesh1").feature("ft").feature("contact").set("hmin", "0.01[mm]");
    model.component("comp1").mesh("mesh1").feature("ft").feature("contact").set("hminactive", true);
    model.component("comp1").mesh("mesh1").feature("ft").feature("roller").set("custom", "on");
    model.component("comp1").mesh("mesh1").feature("ft").feature("roller").set("hmax", "0.75[mm]");
    model.component("comp1").mesh("mesh1").feature("ft").feature("roller").set("hmaxactive", true);
    model.component("comp1").mesh("mesh1").feature("ft").feature("roller").set("hmin", "0.1875[mm]");
    model.component("comp1").mesh("mesh1").feature("ft").feature("roller").set("hminactive", true);
    model.component("comp1").mesh("mesh1").feature("ft").feature("fracture").set("custom", "on");
    model.component("comp1").mesh("mesh1").feature("ft").feature("fracture").set("hmax", "4.0[mm]");
    model.component("comp1").mesh("mesh1").feature("ft").feature("fracture").set("hmaxactive", true);
    model.component("comp1").mesh("mesh1").feature("ft").feature("fracture").set("hmin", "1.0[mm]");
    model.component("comp1").mesh("mesh1").feature("ft").feature("fracture").set("hminactive", true);
    model.component("comp1").mesh("mesh1").run();

    model.study().create("std1");
    model.study("std1").create("stat", "Stationary");
    model.study().create("stdB");
    model.study("stdB").create("stat", "Stationary");

    model.sol().create("sol1");
    model.sol("sol1").study("std1");
    model.sol("sol1").attach("std1");
    model.sol("sol1").create("st1", "StudyStep");
    model.sol("sol1").create("v1", "Variables");
    model.sol("sol1").create("s1", "Stationary");
    model.sol("sol1").feature("s1").create("p1", "Parametric");
    model.sol("sol1").feature("s1").create("fc1", "FullyCoupled");
    model.sol("sol1").feature("s1").feature().remove("fcDef");
    model.sol().create("sol2");
    model.sol("sol2").study("stdB");
    model.sol("sol2").attach("stdB");
    model.sol("sol2").create("st1", "StudyStep");
    model.sol("sol2").create("v1", "Variables");
    model.sol("sol2").create("s1", "Stationary");
    model.sol("sol2").feature("s1").create("p1", "Parametric");
    model.sol("sol2").feature("s1").create("fc1", "FullyCoupled");
    model.sol("sol2").feature("s1").feature().remove("fcDef");

    model.result().dataset().create("dsetB", "Solution");
    model.result().dataset("dsetB").set("solution", "sol2");

    model.study("std1").feature("stat").set("useparam", true);
    model.study("std1").feature("stat").set("pname", new String[]{"dload"});
    model.study("std1").feature("stat").set("plistarr", new String[]{"0.0001 0.0005 0.001 0.002 0.003"});
    model.study("std1").feature("stat").set("punit", new String[]{"mm"});
    model.study("stdB").feature("stat").set("useparam", true);
    model.study("stdB").feature("stat").set("pname", new String[]{"cmod"});
    model.study("stdB").feature("stat")
         .set("plistarr", new String[]{"5e-07 1.5357142857142855e-06 2.571428571428571e-06 3.607142857142857e-06 4.642857142857143e-06 5.678571428571428e-06 6.714285714285714e-06 7.75e-06 8.785714285714286e-06 9.82142857142857e-06 1.0857142857142856e-05 1.1892857142857143e-05 1.2928571428571428e-05 1.3964285714285713e-05 1.5e-05 2e-05 5.3793103448275856e-05 8.758620689655171e-05 0.00012137931034482757 0.00015517241379310343 0.0001889655172413793 0.00022275862068965515 0.00025655172413793103 0.00029034482758620686 0.0003241379310344827 0.0003579310344827586 0.00039172413793103447 0.0004255172413793103 0.00045931034482758613 0.000493103448275862 0.000526896551724138 0.0005606896551724138 0.0005944827586206896 0.0006282758620689654 0.0006620689655172414 0.0006958620689655172 0.000729655172413793 0.000763448275862069 0.0007972413793103448 0.0008310344827586206 0.0008648275862068965 0.0008986206896551723 0.0009324137931034483 0.0009662068965517241 0.001 0.003 0.005 0.007 0.009000000000000001 0.011 0.013000000000000001 0.015 0.017 0.019 0.021 0.023 0.024999999999999998 0.027 0.029 0.031 0.033 0.035 0.037000000000000005 0.03900000000000001 0.041 0.043000000000000003 0.045000000000000005 0.047 0.049 0.051000000000000004 0.053000000000000005 0.05500000000000001 0.057 0.059000000000000004 0.061000000000000006 0.063 0.065 0.067 0.069 0.07100000000000001 0.07300000000000001 0.07500000000000001 0.077 0.079 0.081 0.083 0.085 0.08700000000000001 0.08900000000000001 0.091 0.093 0.095 0.097 0.099 0.101 0.10300000000000001 0.10500000000000001 0.10700000000000001 0.109 0.111 0.113 0.115 0.117 0.11900000000000001 0.12100000000000001 0.123 0.125 0.127 0.129 0.131 0.133 0.135 0.137 0.139 0.14100000000000001 0.14300000000000002 0.14500000000000002 0.14700000000000002 0.149 0.151 0.153 0.155 0.157 0.159 0.161 0.163 0.165 0.167 0.169 0.171 0.17300000000000001 0.17500000000000002 0.17700000000000002 0.179 0.181 0.183 0.185 0.187 0.189 0.191 0.193 0.195 0.197 0.199 0.201 0.203 0.20500000000000002 0.20700000000000002 0.20900000000000002 0.21100000000000002 0.213 0.215 0.217 0.219 0.221 0.223 0.225 0.227 0.229 0.231 0.233 0.23500000000000001 0.23700000000000002 0.23900000000000002 0.24100000000000002 0.243 0.245 0.247 0.249 0.251 0.253 0.255 0.257 0.259 0.261 0.263 0.265 0.267 0.269 0.271 0.273 0.275 0.277 0.279 0.281 0.28300000000000003 0.28500000000000003 0.28700000000000003 0.28900000000000003 0.29100000000000004 0.293 0.295 0.297 0.299 0.301 0.303 0.305 0.307 0.309 0.311 0.313 0.315 0.317 0.319 0.321 0.323 0.325 0.327 0.329 0.331 0.333 0.335 0.337 0.339 0.341 0.343 0.34500000000000003 0.34700000000000003 0.34900000000000003 0.35100000000000003 0.35300000000000004 0.355 0.357 0.359 0.361 0.363 0.365 0.367 0.369 0.371 0.373 0.375 0.377 0.379 0.381 0.383 0.385 0.387 0.389 0.391 0.393 0.395 0.397 0.399 0.401 0.403 0.405 0.40700000000000003 0.40900000000000003 0.41100000000000003 0.41300000000000003 0.41500000000000004 0.41700000000000004 0.41900000000000004 0.421 0.423 0.425 0.427 0.429 0.431 0.433 0.435 0.437 0.439 0.441 0.443 0.445 0.447 0.449 0.451 0.453 0.455 0.457 0.459 0.461 0.463 0.465 0.467 0.46900000000000003 0.47100000000000003 0.47300000000000003 0.47500000000000003 0.47700000000000004 0.47900000000000004 0.48100000000000004 0.483 0.485 0.487 0.489 0.491 0.493 0.495 0.497 0.499 0.501 0.503 0.505 0.507 0.509 0.511 0.513 0.515 0.517 0.519 0.521 0.523 0.525 0.527 0.529 0.531 0.533 0.535 0.537 0.539 0.541 0.543 0.545 0.547 0.549 0.551 0.553 0.555 0.557 0.559 0.561 0.5630000000000001 0.5650000000000001 0.5670000000000001 0.5690000000000001 0.5710000000000001 0.5730000000000001 0.5750000000000001 0.5770000000000001 0.5790000000000001 0.581 0.583 0.585 0.587 0.589 0.591 0.593 0.595 0.597 0.599 0.6"});
    model.study("stdB").feature("stat").set("punit", new String[]{"mm"});

    model.sol("sol1").attach("std1");
    model.sol("sol1").feature("st1").label("Compilar ecuaciones: Estacionario");
    model.sol("sol1").feature("v1").label("Variables dependientes 1.1");
    model.sol("sol1").feature("v1").set("clistctrl", new String[]{"p1"});
    model.sol("sol1").feature("v1").set("cname", new String[]{"dload"});
    model.sol("sol1").feature("v1")
         .set("clist", new String[]{"0.0001[mm] 0.0005[mm] 0.001[mm] 0.002[mm] 0.003[mm]"});
    model.sol("sol1").feature("v1").feature("comp1_solid_wZ").set("scalemethod", "manual");
    model.sol("sol1").feature("v1").feature("comp1_solid_wZ").set("scaleval", "1e-2");
    model.sol("sol1").feature("v1").feature("comp1_u").set("scalemethod", "manual");
    model.sol("sol1").feature("v1").feature("comp1_u").set("scaleval", "1e-2*0.5445410911951457");
    model.sol("sol1").feature("v1").feature("comp1_solid_rd1_u").set("scalemethod", "manual");
    model.sol("sol1").feature("v1").feature("comp1_solid_rd1_u").set("scaleval", "1e-2*0.5445410911951457");
    model.sol("sol1").feature("v1").feature("comp1_solid_rd1_phi").set("scalemethod", "manual");
    model.sol("sol1").feature("v1").feature("comp1_solid_rd1_phi").set("scaleval", "1e-1");
    model.sol("sol1").feature("v1").feature("comp1_solid_rd2_u").set("scalemethod", "manual");
    model.sol("sol1").feature("v1").feature("comp1_solid_rd2_u").set("scaleval", "1e-2*0.5445410911951457");
    model.sol("sol1").feature("v1").feature("comp1_solid_rd2_phi").set("scalemethod", "manual");
    model.sol("sol1").feature("v1").feature("comp1_solid_rd2_phi").set("scaleval", "1e-1");
    model.sol("sol1").feature("v1").feature("comp1_solid_rd3_u").set("scalemethod", "manual");
    model.sol("sol1").feature("v1").feature("comp1_solid_rd3_u").set("scaleval", "1e-2*0.5445410911951457");

    return model;
  }

  public static Model run2(Model model) {
    model.sol("sol1").feature("v1").feature("comp1_solid_rd3_phi").set("scalemethod", "manual");
    model.sol("sol1").feature("v1").feature("comp1_solid_rd3_phi").set("scaleval", "1e-1");
    model.sol("sol1").feature("s1").label("Resolvedor estacionario 1.1");
    model.sol("sol1").feature("s1").set("stol", "1e-6");
    model.sol("sol1").feature("s1").set("probesel", "none");
    model.sol("sol1").feature("s1").feature("dDef").label("Directo 1");
    model.sol("sol1").feature("s1").feature("aDef").label("Avanzado 1");
    model.sol("sol1").feature("s1").feature("aDef").set("cachepattern", true);
    model.sol("sol1").feature("s1").feature("p1").label("Param\u00e9trico 1.1");
    model.sol("sol1").feature("s1").feature("p1").set("pname", new String[]{"dload"});
    model.sol("sol1").feature("s1").feature("p1").set("plistarr", new String[]{"0.0001 0.0005 0.001 0.002 0.003"});
    model.sol("sol1").feature("s1").feature("p1").set("punit", new String[]{"mm"});
    model.sol("sol1").feature("s1").feature("p1").set("porder", "constant");
    model.sol("sol1").feature("s1").feature("fc1").label("Completamente acoplado 1.1");
    model.sol("sol1").feature("s1").feature("fc1").set("initstep", 0.5);
    model.sol("sol1").feature("s1").feature("fc1").set("minstep", "1e-5");
    model.sol("sol1").feature("s1").feature("fc1").set("maxiter", 60);
    model.sol("sol1").runAll();
    model.sol("sol2").attach("stdB");
    model.sol("sol2").feature("st1").label("Compilar ecuaciones: Estacionario");
    model.sol("sol2").feature("v1").label("Variables dependientes 1.1");
    model.sol("sol2").feature("v1").set("control", "user");
    model.sol("sol2").feature("v1").set("initmethod", "sol");
    model.sol("sol2").feature("v1").set("initsol", "sol1");
    model.sol("sol2").feature("v1").set("solnum", "last");
    model.sol("sol2").feature("v1").set("clistctrl", new String[]{"p1"});
    model.sol("sol2").feature("v1").set("cname", new String[]{"cmod"});
    model.sol("sol2").feature("v1")
         .set("clist", new String[]{"5e-07[mm] 1.5357142857142855e-06[mm] 2.571428571428571e-06[mm] 3.607142857142857e-06[mm] 4.642857142857143e-06[mm] 5.678571428571428e-06[mm] 6.714285714285714e-06[mm] 7.75e-06[mm] 8.785714285714286e-06[mm] 9.82142857142857e-06[mm] 1.0857142857142856e-05[mm] 1.1892857142857143e-05[mm] 1.2928571428571428e-05[mm] 1.3964285714285713e-05[mm] 1.5e-05[mm] 2e-05[mm] 5.3793103448275856e-05[mm] 8.758620689655171e-05[mm] 0.00012137931034482757[mm] 0.00015517241379310343[mm] 0.0001889655172413793[mm] 0.00022275862068965515[mm] 0.00025655172413793103[mm] 0.00029034482758620686[mm] 0.0003241379310344827[mm] 0.0003579310344827586[mm] 0.00039172413793103447[mm] 0.0004255172413793103[mm] 0.00045931034482758613[mm] 0.000493103448275862[mm] 0.000526896551724138[mm] 0.0005606896551724138[mm] 0.0005944827586206896[mm] 0.0006282758620689654[mm] 0.0006620689655172414[mm] 0.0006958620689655172[mm] 0.000729655172413793[mm] 0.000763448275862069[mm] 0.0007972413793103448[mm] 0.0008310344827586206[mm] 0.0008648275862068965[mm] 0.0008986206896551723[mm] 0.0009324137931034483[mm] 0.0009662068965517241[mm] 0.001[mm] 0.003[mm] 0.005[mm] 0.007[mm] 0.009000000000000001[mm] 0.011[mm] 0.013000000000000001[mm] 0.015[mm] 0.017[mm] 0.019[mm] 0.021[mm] 0.023[mm] 0.024999999999999998[mm] 0.027[mm] 0.029[mm] 0.031[mm] 0.033[mm] 0.035[mm] 0.037000000000000005[mm] 0.03900000000000001[mm] 0.041[mm] 0.043000000000000003[mm] 0.045000000000000005[mm] 0.047[mm] 0.049[mm] 0.051000000000000004[mm] 0.053000000000000005[mm] 0.05500000000000001[mm] 0.057[mm] 0.059000000000000004[mm] 0.061000000000000006[mm] 0.063[mm] 0.065[mm] 0.067[mm] 0.069[mm] 0.07100000000000001[mm] 0.07300000000000001[mm] 0.07500000000000001[mm] 0.077[mm] 0.079[mm] 0.081[mm] 0.083[mm] 0.085[mm] 0.08700000000000001[mm] 0.08900000000000001[mm] 0.091[mm] 0.093[mm] 0.095[mm] 0.097[mm] 0.099[mm] 0.101[mm] 0.10300000000000001[mm] 0.10500000000000001[mm] 0.10700000000000001[mm] 0.109[mm] 0.111[mm] 0.113[mm] 0.115[mm] 0.117[mm] 0.11900000000000001[mm] 0.12100000000000001[mm] 0.123[mm] 0.125[mm] 0.127[mm] 0.129[mm] 0.131[mm] 0.133[mm] 0.135[mm] 0.137[mm] 0.139[mm] 0.14100000000000001[mm] 0.14300000000000002[mm] 0.14500000000000002[mm] 0.14700000000000002[mm] 0.149[mm] 0.151[mm] 0.153[mm] 0.155[mm] 0.157[mm] 0.159[mm] 0.161[mm] 0.163[mm] 0.165[mm] 0.167[mm] 0.169[mm] 0.171[mm] 0.17300000000000001[mm] 0.17500000000000002[mm] 0.17700000000000002[mm] 0.179[mm] 0.181[mm] 0.183[mm] 0.185[mm] 0.187[mm] 0.189[mm] 0.191[mm] 0.193[mm] 0.195[mm] 0.197[mm] 0.199[mm] 0.201[mm] 0.203[mm] 0.20500000000000002[mm] 0.20700000000000002[mm] 0.20900000000000002[mm] 0.21100000000000002[mm] 0.213[mm] 0.215[mm] 0.217[mm] 0.219[mm] 0.221[mm] 0.223[mm] 0.225[mm] 0.227[mm] 0.229[mm] 0.231[mm] 0.233[mm] 0.23500000000000001[mm] 0.23700000000000002[mm] 0.23900000000000002[mm] 0.24100000000000002[mm] 0.243[mm] 0.245[mm] 0.247[mm] 0.249[mm] 0.251[mm] 0.253[mm] 0.255[mm] 0.257[mm] 0.259[mm] 0.261[mm] 0.263[mm] 0.265[mm] 0.267[mm] 0.269[mm] 0.271[mm] 0.273[mm] 0.275[mm] 0.277[mm] 0.279[mm] 0.281[mm] 0.28300000000000003[mm] 0.28500000000000003[mm] 0.28700000000000003[mm] 0.28900000000000003[mm] 0.29100000000000004[mm] 0.293[mm] 0.295[mm] 0.297[mm] 0.299[mm] 0.301[mm] 0.303[mm] 0.305[mm] 0.307[mm] 0.309[mm] 0.311[mm] 0.313[mm] 0.315[mm] 0.317[mm] 0.319[mm] 0.321[mm] 0.323[mm] 0.325[mm] 0.327[mm] 0.329[mm] 0.331[mm] 0.333[mm] 0.335[mm] 0.337[mm] 0.339[mm] 0.341[mm] 0.343[mm] 0.34500000000000003[mm] 0.34700000000000003[mm] 0.34900000000000003[mm] 0.35100000000000003[mm] 0.35300000000000004[mm] 0.355[mm] 0.357[mm] 0.359[mm] 0.361[mm] 0.363[mm] 0.365[mm] 0.367[mm] 0.369[mm] 0.371[mm] 0.373[mm] 0.375[mm] 0.377[mm] 0.379[mm] 0.381[mm] 0.383[mm] 0.385[mm] 0.387[mm] 0.389[mm] 0.391[mm] 0.393[mm] 0.395[mm] 0.397[mm] 0.399[mm] 0.401[mm] 0.403[mm] 0.405[mm] 0.40700000000000003[mm] 0.40900000000000003[mm] 0.41100000000000003[mm] 0.41300000000000003[mm] 0.41500000000000004[mm] 0.41700000000000004[mm] 0.41900000000000004[mm] 0.421[mm] 0.423[mm] 0.425[mm] 0.427[mm] 0.429[mm] 0.431[mm] 0.433[mm] 0.435[mm] 0.437[mm] 0.439[mm] 0.441[mm] 0.443[mm] 0.445[mm] 0.447[mm] 0.449[mm] 0.451[mm] 0.453[mm] 0.455[mm] 0.457[mm] 0.459[mm] 0.461[mm] 0.463[mm] 0.465[mm] 0.467[mm] 0.46900000000000003[mm] 0.47100000000000003[mm] 0.47300000000000003[mm] 0.47500000000000003[mm] 0.47700000000000004[mm] 0.47900000000000004[mm] 0.48100000000000004[mm] 0.483[mm] 0.485[mm] 0.487[mm] 0.489[mm] 0.491[mm] 0.493[mm] 0.495[mm] 0.497[mm] 0.499[mm] 0.501[mm] 0.503[mm] 0.505[mm] 0.507[mm] 0.509[mm] 0.511[mm] 0.513[mm] 0.515[mm] 0.517[mm] 0.519[mm] 0.521[mm] 0.523[mm] 0.525[mm] 0.527[mm] 0.529[mm] 0.531[mm] 0.533[mm] 0.535[mm] 0.537[mm] 0.539[mm] 0.541[mm] 0.543[mm] 0.545[mm] 0.547[mm] 0.549[mm] 0.551[mm] 0.553[mm] 0.555[mm] 0.557[mm] 0.559[mm] 0.561[mm] 0.5630000000000001[mm] 0.5650000000000001[mm] 0.5670000000000001[mm] 0.5690000000000001[mm] 0.5710000000000001[mm] 0.5730000000000001[mm] 0.5750000000000001[mm] 0.5770000000000001[mm] 0.5790000000000001[mm] 0.581[mm] 0.583[mm] 0.585[mm] 0.587[mm] 0.589[mm] 0.591[mm] 0.593[mm] 0.595[mm] 0.597[mm] 0.599[mm] 0.6[mm]"});
    model.sol("sol2").feature("v1").feature("comp1_solid_wZ").set("scalemethod", "manual");
    model.sol("sol2").feature("v1").feature("comp1_solid_wZ").set("scaleval", "1e-2");
    model.sol("sol2").feature("v1").feature("comp1_u").set("scalemethod", "manual");
    model.sol("sol2").feature("v1").feature("comp1_u").set("scaleval", "1e-2*0.5445410911951457");
    model.sol("sol2").feature("v1").feature("comp1_solid_rd1_u").set("scalemethod", "manual");
    model.sol("sol2").feature("v1").feature("comp1_solid_rd1_u").set("scaleval", "1e-2*0.5445410911951457");
    model.sol("sol2").feature("v1").feature("comp1_solid_rd1_phi").set("scalemethod", "manual");
    model.sol("sol2").feature("v1").feature("comp1_solid_rd1_phi").set("scaleval", "1e-1");
    model.sol("sol2").feature("v1").feature("comp1_solid_rd2_u").set("scalemethod", "manual");
    model.sol("sol2").feature("v1").feature("comp1_solid_rd2_u").set("scaleval", "1e-2*0.5445410911951457");
    model.sol("sol2").feature("v1").feature("comp1_solid_rd2_phi").set("scalemethod", "manual");
    model.sol("sol2").feature("v1").feature("comp1_solid_rd2_phi").set("scaleval", "1e-1");
    model.sol("sol2").feature("v1").feature("comp1_solid_rd3_u").set("scalemethod", "manual");
    model.sol("sol2").feature("v1").feature("comp1_solid_rd3_u").set("scaleval", "1e-2*0.5445410911951457");
    model.sol("sol2").feature("v1").feature("comp1_solid_rd3_phi").set("scalemethod", "manual");
    model.sol("sol2").feature("v1").feature("comp1_solid_rd3_phi").set("scaleval", "1e-1");
    model.sol("sol2").feature("s1").label("Resolvedor estacionario 1.1");
    model.sol("sol2").feature("s1").set("stol", "1e-6");
    model.sol("sol2").feature("s1").set("probesel", "none");
    model.sol("sol2").feature("s1").feature("dDef").label("Directo 1");
    model.sol("sol2").feature("s1").feature("aDef").label("Avanzado 1");
    model.sol("sol2").feature("s1").feature("aDef").set("cachepattern", true);
    model.sol("sol2").feature("s1").feature("p1").label("Param\u00e9trico 1.1");
    model.sol("sol2").feature("s1").feature("p1").set("pname", new String[]{"cmod"});
    model.sol("sol2").feature("s1").feature("p1")
         .set("plistarr", new String[]{"5e-07 1.5357142857142855e-06 2.571428571428571e-06 3.607142857142857e-06 4.642857142857143e-06 5.678571428571428e-06 6.714285714285714e-06 7.75e-06 8.785714285714286e-06 9.82142857142857e-06 1.0857142857142856e-05 1.1892857142857143e-05 1.2928571428571428e-05 1.3964285714285713e-05 1.5e-05 2e-05 5.3793103448275856e-05 8.758620689655171e-05 0.00012137931034482757 0.00015517241379310343 0.0001889655172413793 0.00022275862068965515 0.00025655172413793103 0.00029034482758620686 0.0003241379310344827 0.0003579310344827586 0.00039172413793103447 0.0004255172413793103 0.00045931034482758613 0.000493103448275862 0.000526896551724138 0.0005606896551724138 0.0005944827586206896 0.0006282758620689654 0.0006620689655172414 0.0006958620689655172 0.000729655172413793 0.000763448275862069 0.0007972413793103448 0.0008310344827586206 0.0008648275862068965 0.0008986206896551723 0.0009324137931034483 0.0009662068965517241 0.001 0.003 0.005 0.007 0.009000000000000001 0.011 0.013000000000000001 0.015 0.017 0.019 0.021 0.023 0.024999999999999998 0.027 0.029 0.031 0.033 0.035 0.037000000000000005 0.03900000000000001 0.041 0.043000000000000003 0.045000000000000005 0.047 0.049 0.051000000000000004 0.053000000000000005 0.05500000000000001 0.057 0.059000000000000004 0.061000000000000006 0.063 0.065 0.067 0.069 0.07100000000000001 0.07300000000000001 0.07500000000000001 0.077 0.079 0.081 0.083 0.085 0.08700000000000001 0.08900000000000001 0.091 0.093 0.095 0.097 0.099 0.101 0.10300000000000001 0.10500000000000001 0.10700000000000001 0.109 0.111 0.113 0.115 0.117 0.11900000000000001 0.12100000000000001 0.123 0.125 0.127 0.129 0.131 0.133 0.135 0.137 0.139 0.14100000000000001 0.14300000000000002 0.14500000000000002 0.14700000000000002 0.149 0.151 0.153 0.155 0.157 0.159 0.161 0.163 0.165 0.167 0.169 0.171 0.17300000000000001 0.17500000000000002 0.17700000000000002 0.179 0.181 0.183 0.185 0.187 0.189 0.191 0.193 0.195 0.197 0.199 0.201 0.203 0.20500000000000002 0.20700000000000002 0.20900000000000002 0.21100000000000002 0.213 0.215 0.217 0.219 0.221 0.223 0.225 0.227 0.229 0.231 0.233 0.23500000000000001 0.23700000000000002 0.23900000000000002 0.24100000000000002 0.243 0.245 0.247 0.249 0.251 0.253 0.255 0.257 0.259 0.261 0.263 0.265 0.267 0.269 0.271 0.273 0.275 0.277 0.279 0.281 0.28300000000000003 0.28500000000000003 0.28700000000000003 0.28900000000000003 0.29100000000000004 0.293 0.295 0.297 0.299 0.301 0.303 0.305 0.307 0.309 0.311 0.313 0.315 0.317 0.319 0.321 0.323 0.325 0.327 0.329 0.331 0.333 0.335 0.337 0.339 0.341 0.343 0.34500000000000003 0.34700000000000003 0.34900000000000003 0.35100000000000003 0.35300000000000004 0.355 0.357 0.359 0.361 0.363 0.365 0.367 0.369 0.371 0.373 0.375 0.377 0.379 0.381 0.383 0.385 0.387 0.389 0.391 0.393 0.395 0.397 0.399 0.401 0.403 0.405 0.40700000000000003 0.40900000000000003 0.41100000000000003 0.41300000000000003 0.41500000000000004 0.41700000000000004 0.41900000000000004 0.421 0.423 0.425 0.427 0.429 0.431 0.433 0.435 0.437 0.439 0.441 0.443 0.445 0.447 0.449 0.451 0.453 0.455 0.457 0.459 0.461 0.463 0.465 0.467 0.46900000000000003 0.47100000000000003 0.47300000000000003 0.47500000000000003 0.47700000000000004 0.47900000000000004 0.48100000000000004 0.483 0.485 0.487 0.489 0.491 0.493 0.495 0.497 0.499 0.501 0.503 0.505 0.507 0.509 0.511 0.513 0.515 0.517 0.519 0.521 0.523 0.525 0.527 0.529 0.531 0.533 0.535 0.537 0.539 0.541 0.543 0.545 0.547 0.549 0.551 0.553 0.555 0.557 0.559 0.561 0.5630000000000001 0.5650000000000001 0.5670000000000001 0.5690000000000001 0.5710000000000001 0.5730000000000001 0.5750000000000001 0.5770000000000001 0.5790000000000001 0.581 0.583 0.585 0.587 0.589 0.591 0.593 0.595 0.597 0.599 0.6"});
    model.sol("sol2").feature("s1").feature("p1").set("punit", new String[]{"mm"});
    model.sol("sol2").feature("s1").feature("p1").set("porder", "constant");
    model.sol("sol2").feature("s1").feature("fc1").label("Completamente acoplado 1.1");
    model.sol("sol2").feature("s1").feature("fc1").set("minstep", "1e-6");
    model.sol("sol2").feature("s1").feature("fc1").set("maxiter", 80);
    model.sol("sol2").runAll();

    return model;
  }

  public static void main(String[] args) {
    Model model = run();
    run2(model);
  }

}
