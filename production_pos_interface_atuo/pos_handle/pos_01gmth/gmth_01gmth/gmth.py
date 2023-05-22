from tools.decorfun import fun_info_name
from pos_handle.pos_01gmth.gmth_01gmth.gmth_handle.pay.tmlPayDtl import tmlPayDtl
from pos_handle.pos_01gmth.gmth_01gmth.gmth_handle.tmlinfo_print.tmlinfo_print import tmlinfo_print
from pos_handle.pos_01gmth.gmth_01gmth.tuihuo.refundTmlPayForPos import refundTmlPayForPos


def gmth():
    tmlPayDtl()
    tmlinfo_print()
    refundTmlPayForPos()
