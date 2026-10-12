import verificar_czm as z
import mph
mph.option('session','stand-alone');client=mph.start(version='6.1',cores=2)
for h,kind in [(1.25,'tension'),(.625,'tension'),(1.25,'compression'),(1.25,'cycle')]:z.coupon(client,h,kind)
