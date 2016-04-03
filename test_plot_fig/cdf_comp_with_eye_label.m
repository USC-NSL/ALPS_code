xa = [12.90133333, 7.39, 2.93, 15.28869073, 14.75063483, 13.89340188, 13.73845297, 13.44444113, 12.78331659, 11.08528867, 9.652217646, 9.61904877, 9.493440329, 9.404195569, 9.309208769, 9.293083232, 9.283588616, 9.04501182, 8.835210973, 8.817426867, 8.814928755, 8.799037568, 8.73098645, 8.195362682, 8.097200297, 8.05281845, 7.847026006, 7.631175918, 7.348894705, 7.305667347, 7.292574144, 7.013194212, 6.91374115, 6.664487379, 6.351489579, 6.324416743, 6.309859146, 6.082211126, 6.075945173, 6.017290051, 5.954158187, 5.886117539, 5.870886524, 5.840035354, 5.776930233, 5.772192023, 5.686399964, 5.610804476, 5.541721639, 5.402148134, 5.396720751, 5.341739453, 5.325391234, 5.303290403, 5.215641911, 5.01229593, 4.970992342, 4.950517214, 4.945461394, 4.892624784, 4.861494234, 4.772512269, 4.740802523, 4.679402233, 4.61733964, 4.519316912, 4.480369269, 4.479962199, 4.476599237, 4.469978723, 4.417349272, 4.23850544, 4.220295515, 4.097357108, 4.082543977, 4.04003456, 4.028047833, 3.983056126, 3.762417427, 3.713653865, 3.704753242, 3.68708871, 3.607852795, 3.579996836, 3.30542288, 3.080087819, 2.822813291, 2.797500375, 2.7655897, 2.760757356, 2.528550196, 2.508955612, 2.47991215, 2.395803619, 2.240673195, 2.201143384, 2.101384354, 2.092148308, 2.063747835, 2.024967098, 2.018557764, 2.000379607, 1.992630644, 1.992414886, 1.885185431, 1.880440026, 1.865946419, 1.714265369, 1.606713033, 1.523857659, 1.372261991, 1.3313131, 1.31668594, 1.151113319, 1.027457993];
xm = [0.690728832, 0.746283775, 0.796532581, 0.887972622, 0.889055103, 0.982790598, 1.217447264, 1.224138332, 1.235092618, 1.471039695, 1.525540418, 1.582370836, 1.649415761, 1.715365848, 1.949611265, 2.001601854, 2.030613391, 2.069784429, 2.632161773, 2.650797444, 2.665598208, 2.740194515, 2.747627882, 2.852540572, 3.045528845, 3.103217753, 3.142992102, 3.173538855, 3.176901524, 3.364992275, 3.443477332, 3.452353917, 3.624167204, 3.838494176, 3.864003702, 4.116974931, 4.124575374, 4.179414637, 4.381868991, 4.517353006, 4.616489211, 4.722592791, 4.811205799, 4.888368743, 4.90404727, 4.947582777, 4.977661906, 5.042992161, 5.046783491, 5.068566379, 5.159750536, 5.299587875, 5.401632235, 5.406503399, 5.515229839, 5.627094639, 5.757280079, 5.780851391, 5.818691508, 6.082627541, 6.084881206, 6.203777012, 6.222390856, 6.416607519, 6.533318758, 6.577652026, 6.794540719, 6.971351938, 7.142775378, 7.157573118, 7.206285057, 7.457589844, 7.500684717, 7.551064926, 7.969606103, 8.193295744, 8.449386372, 8.450925847, 8.482889973, 8.701022298, 9.035114188, 9.313600951, 9.598404707, 9.670570646, 10.53986540, 10.13454575, 10.35675578, 10.50890092, 13.07585455, 13.58362340, 14.12332035, 14.93554789, 15.2012056];

sa = sort(xa);
sm = sort(xm);

h = subplot(1, 1, 1);
set(h, 'FontSize', 22, 'FontName', 'Times New Roman');
hold on;

p = plot(sa, (0.5:length(sa))./length(sa), '-');
set(p, 'Color', 'blue', 'LineWidth', 2, 'markers', 8);

p = plot(sm, (0.5:length(sm))./length(sm), '-');
set(p, 'Color', 'green', 'LineWidth', 2, 'markers', 8);

axis([0 20 0 1]);

box on;

legend('ALPS w/o ideal detector', 'ALPS w/ ideal detector', 'Location', 'southeast');
xlabel('error(m)');
ylabel('CDF');

filename = ['cdf_comp_with_eye_label.eps'];
saveas(h, filename, 'epsc2');