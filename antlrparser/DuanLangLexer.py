# Generated from g:\dumategithub\duan\antlrparser\DuanLang.g4 by ANTLR 4.9.2
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
    from typing import TextIO
else:
    from typing.io import TextIO


import sys
from antlr4 import *
from typing import List, Optional, Tuple, Any, Union



def serializedATN():
    with StringIO() as buf:
        buf.write("\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\2d")
        buf.write("\u020c\b\1\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7")
        buf.write("\t\7\4\b\t\b\4\t\t\t\4\n\t\n\4\13\t\13\4\f\t\f\4\r\t\r")
        buf.write("\4\16\t\16\4\17\t\17\4\20\t\20\4\21\t\21\4\22\t\22\4\23")
        buf.write("\t\23\4\24\t\24\4\25\t\25\4\26\t\26\4\27\t\27\4\30\t\30")
        buf.write("\4\31\t\31\4\32\t\32\4\33\t\33\4\34\t\34\4\35\t\35\4\36")
        buf.write("\t\36\4\37\t\37\4 \t \4!\t!\4\"\t\"\4#\t#\4$\t$\4%\t%")
        buf.write("\4&\t&\4\'\t\'\4(\t(\4)\t)\4*\t*\4+\t+\4,\t,\4-\t-\4.")
        buf.write("\t.\4/\t/\4\60\t\60\4\61\t\61\4\62\t\62\4\63\t\63\4\64")
        buf.write("\t\64\4\65\t\65\4\66\t\66\4\67\t\67\48\t8\49\t9\4:\t:")
        buf.write("\4;\t;\4<\t<\4=\t=\4>\t>\4?\t?\4@\t@\4A\tA\4B\tB\4C\t")
        buf.write("C\4D\tD\4E\tE\4F\tF\4G\tG\4H\tH\4I\tI\4J\tJ\4K\tK\4L\t")
        buf.write("L\4M\tM\4N\tN\4O\tO\4P\tP\4Q\tQ\4R\tR\4S\tS\4T\tT\4U\t")
        buf.write("U\4V\tV\4W\tW\4X\tX\4Y\tY\4Z\tZ\4[\t[\4\\\t\\\4]\t]\4")
        buf.write("^\t^\4_\t_\4`\t`\4a\ta\4b\tb\4c\tc\4d\td\4e\te\4f\tf\3")
        buf.write("\2\3\2\3\2\3\2\3\2\7\2\u00d3\n\2\f\2\16\2\u00d6\13\2\3")
        buf.write("\2\3\2\3\2\3\2\3\2\3\2\3\3\3\3\3\3\3\3\3\4\3\4\3\4\3\5")
        buf.write("\3\5\3\5\3\6\3\6\3\6\3\7\3\7\3\7\3\b\3\b\3\b\3\b\3\b\3")
        buf.write("\t\3\t\3\t\3\t\3\t\3\n\3\n\3\n\3\n\3\13\3\13\3\13\3\f")
        buf.write("\3\f\3\f\3\r\3\r\3\r\3\16\3\16\3\16\3\17\3\17\3\20\3\20")
        buf.write("\3\21\3\21\3\21\3\22\3\22\3\23\3\23\3\23\3\23\3\23\3\24")
        buf.write("\3\24\3\24\3\25\3\25\3\25\3\26\3\26\3\26\3\27\3\27\3\27")
        buf.write("\3\30\3\30\3\30\3\31\3\31\3\32\3\32\3\32\3\33\3\33\3\34")
        buf.write("\3\34\3\34\3\35\3\35\3\35\3\36\3\36\3\36\3\37\3\37\3\37")
        buf.write("\3 \3 \3 \3!\3!\3!\3\"\3\"\3\"\3#\3#\3#\3$\3$\3$\3%\3")
        buf.write("%\3%\3&\3&\3&\3\'\3\'\3(\3(\3(\3)\3)\3)\3*\3*\3+\3+\3")
        buf.write(",\3,\3-\3-\3.\3.\3/\3/\3\60\3\60\3\61\3\61\3\62\3\62\3")
        buf.write("\63\3\63\3\64\3\64\3\65\3\65\3\66\3\66\3\67\3\67\38\3")
        buf.write("8\39\39\3:\3:\3:\3;\3;\3;\3<\3<\3=\3=\3>\3>\3?\3?\3@\3")
        buf.write("@\3@\3A\3A\3A\3B\3B\3C\3C\3D\3D\3E\3E\3F\3F\3G\3G\3H\3")
        buf.write("H\3H\3I\3I\3I\3J\3J\3J\3K\3K\3K\3L\3L\3M\3M\3N\3N\3O\3")
        buf.write("O\3O\3P\3P\3P\3Q\3Q\3Q\3R\3R\3S\3S\3T\3T\3U\3U\3V\3V\3")
        buf.write("W\3W\3X\3X\3Y\3Y\3Z\3Z\3[\3[\3\\\3\\\3]\3]\3^\6^\u01c9")
        buf.write("\n^\r^\16^\u01ca\3^\3^\6^\u01cf\n^\r^\16^\u01d0\5^\u01d3")
        buf.write("\n^\3_\3_\3_\3_\7_\u01d9\n_\f_\16_\u01dc\13_\3_\3_\3_")
        buf.write("\3_\3_\7_\u01e3\n_\f_\16_\u01e6\13_\3_\5_\u01e9\n_\3`")
        buf.write("\3`\3a\3a\3b\3b\3c\3c\5c\u01f3\nc\3c\3c\3c\7c\u01f8\n")
        buf.write("c\fc\16c\u01fb\13c\3d\5d\u01fe\nd\3d\3d\3d\3d\3e\6e\u0205")
        buf.write("\ne\re\16e\u0206\3e\3e\3f\3f\3\u00d4\2g\3\3\5\4\7\5\t")
        buf.write("\6\13\7\r\b\17\t\21\n\23\13\25\f\27\r\31\16\33\17\35\20")
        buf.write("\37\21!\22#\23%\24\'\25)\26+\27-\30/\31\61\32\63\33\65")
        buf.write("\34\67\359\36;\37= ?!A\"C#E$G%I&K\'M(O)Q*S+U,W-Y.[/]\60")
        buf.write("_\61a\62c\63e\64g\65i\66k\67m8o9q:s;u<w=y>{?}@\177A\u0081")
        buf.write("B\u0083C\u0085D\u0087E\u0089F\u008bG\u008dH\u008fI\u0091")
        buf.write("J\u0093K\u0095L\u0097M\u0099N\u009bO\u009dP\u009fQ\u00a1")
        buf.write("R\u00a3S\u00a5T\u00a7U\u00a9V\u00abW\u00adX\u00afY\u00b1")
        buf.write("Z\u00b3[\u00b5\\\u00b7]\u00b9^\u00bb_\u00bd`\u00bf\2\u00c1")
        buf.write("\2\u00c3\2\u00c5a\u00c7b\u00c9c\u00cbd\3\2\21\4\2\61\61")
        buf.write("\uff11\uff11\4\2\60\60\u3004\u3004\4\2..\uff0e\uff0e\4")
        buf.write("\2<<\uff1c\uff1c\4\2==\uff1d\uff1d\4\2**\uff0a\uff0a\4")
        buf.write("\2++\uff0b\uff0b\4\2]]\u3012\u3012\4\2__\u3013\u3013\3")
        buf.write("\2\62;\4\2$$^^\4\2))^^\5\2\u3402\u4dc1\u4e02\ua001\uf902")
        buf.write("\ufb01\5\2C\\aac|\5\2\13\f\17\17\"\"\2\u0217\2\3\3\2\2")
        buf.write("\2\2\5\3\2\2\2\2\7\3\2\2\2\2\t\3\2\2\2\2\13\3\2\2\2\2")
        buf.write("\r\3\2\2\2\2\17\3\2\2\2\2\21\3\2\2\2\2\23\3\2\2\2\2\25")
        buf.write("\3\2\2\2\2\27\3\2\2\2\2\31\3\2\2\2\2\33\3\2\2\2\2\35\3")
        buf.write("\2\2\2\2\37\3\2\2\2\2!\3\2\2\2\2#\3\2\2\2\2%\3\2\2\2\2")
        buf.write("\'\3\2\2\2\2)\3\2\2\2\2+\3\2\2\2\2-\3\2\2\2\2/\3\2\2\2")
        buf.write("\2\61\3\2\2\2\2\63\3\2\2\2\2\65\3\2\2\2\2\67\3\2\2\2\2")
        buf.write("9\3\2\2\2\2;\3\2\2\2\2=\3\2\2\2\2?\3\2\2\2\2A\3\2\2\2")
        buf.write("\2C\3\2\2\2\2E\3\2\2\2\2G\3\2\2\2\2I\3\2\2\2\2K\3\2\2")
        buf.write("\2\2M\3\2\2\2\2O\3\2\2\2\2Q\3\2\2\2\2S\3\2\2\2\2U\3\2")
        buf.write("\2\2\2W\3\2\2\2\2Y\3\2\2\2\2[\3\2\2\2\2]\3\2\2\2\2_\3")
        buf.write("\2\2\2\2a\3\2\2\2\2c\3\2\2\2\2e\3\2\2\2\2g\3\2\2\2\2i")
        buf.write("\3\2\2\2\2k\3\2\2\2\2m\3\2\2\2\2o\3\2\2\2\2q\3\2\2\2\2")
        buf.write("s\3\2\2\2\2u\3\2\2\2\2w\3\2\2\2\2y\3\2\2\2\2{\3\2\2\2")
        buf.write("\2}\3\2\2\2\2\177\3\2\2\2\2\u0081\3\2\2\2\2\u0083\3\2")
        buf.write("\2\2\2\u0085\3\2\2\2\2\u0087\3\2\2\2\2\u0089\3\2\2\2\2")
        buf.write("\u008b\3\2\2\2\2\u008d\3\2\2\2\2\u008f\3\2\2\2\2\u0091")
        buf.write("\3\2\2\2\2\u0093\3\2\2\2\2\u0095\3\2\2\2\2\u0097\3\2\2")
        buf.write("\2\2\u0099\3\2\2\2\2\u009b\3\2\2\2\2\u009d\3\2\2\2\2\u009f")
        buf.write("\3\2\2\2\2\u00a1\3\2\2\2\2\u00a3\3\2\2\2\2\u00a5\3\2\2")
        buf.write("\2\2\u00a7\3\2\2\2\2\u00a9\3\2\2\2\2\u00ab\3\2\2\2\2\u00ad")
        buf.write("\3\2\2\2\2\u00af\3\2\2\2\2\u00b1\3\2\2\2\2\u00b3\3\2\2")
        buf.write("\2\2\u00b5\3\2\2\2\2\u00b7\3\2\2\2\2\u00b9\3\2\2\2\2\u00bb")
        buf.write("\3\2\2\2\2\u00bd\3\2\2\2\2\u00c5\3\2\2\2\2\u00c7\3\2\2")
        buf.write("\2\2\u00c9\3\2\2\2\2\u00cb\3\2\2\2\3\u00cd\3\2\2\2\5\u00dd")
        buf.write("\3\2\2\2\7\u00e1\3\2\2\2\t\u00e4\3\2\2\2\13\u00e7\3\2")
        buf.write("\2\2\r\u00ea\3\2\2\2\17\u00ed\3\2\2\2\21\u00f2\3\2\2\2")
        buf.write("\23\u00f7\3\2\2\2\25\u00fb\3\2\2\2\27\u00fe\3\2\2\2\31")
        buf.write("\u0101\3\2\2\2\33\u0104\3\2\2\2\35\u0107\3\2\2\2\37\u0109")
        buf.write("\3\2\2\2!\u010b\3\2\2\2#\u010e\3\2\2\2%\u0110\3\2\2\2")
        buf.write("\'\u0115\3\2\2\2)\u0118\3\2\2\2+\u011b\3\2\2\2-\u011e")
        buf.write("\3\2\2\2/\u0121\3\2\2\2\61\u0124\3\2\2\2\63\u0126\3\2")
        buf.write("\2\2\65\u0129\3\2\2\2\67\u012b\3\2\2\29\u012e\3\2\2\2")
        buf.write(";\u0131\3\2\2\2=\u0134\3\2\2\2?\u0137\3\2\2\2A\u013a\3")
        buf.write("\2\2\2C\u013d\3\2\2\2E\u0140\3\2\2\2G\u0143\3\2\2\2I\u0146")
        buf.write("\3\2\2\2K\u0149\3\2\2\2M\u014c\3\2\2\2O\u014e\3\2\2\2")
        buf.write("Q\u0151\3\2\2\2S\u0154\3\2\2\2U\u0156\3\2\2\2W\u0158\3")
        buf.write("\2\2\2Y\u015a\3\2\2\2[\u015c\3\2\2\2]\u015e\3\2\2\2_\u0160")
        buf.write("\3\2\2\2a\u0162\3\2\2\2c\u0164\3\2\2\2e\u0166\3\2\2\2")
        buf.write("g\u0168\3\2\2\2i\u016a\3\2\2\2k\u016c\3\2\2\2m\u016e\3")
        buf.write("\2\2\2o\u0170\3\2\2\2q\u0172\3\2\2\2s\u0174\3\2\2\2u\u0177")
        buf.write("\3\2\2\2w\u017a\3\2\2\2y\u017c\3\2\2\2{\u017e\3\2\2\2")
        buf.write("}\u0180\3\2\2\2\177\u0182\3\2\2\2\u0081\u0185\3\2\2\2")
        buf.write("\u0083\u0188\3\2\2\2\u0085\u018a\3\2\2\2\u0087\u018c\3")
        buf.write("\2\2\2\u0089\u018e\3\2\2\2\u008b\u0190\3\2\2\2\u008d\u0192")
        buf.write("\3\2\2\2\u008f\u0194\3\2\2\2\u0091\u0197\3\2\2\2\u0093")
        buf.write("\u019a\3\2\2\2\u0095\u019d\3\2\2\2\u0097\u01a0\3\2\2\2")
        buf.write("\u0099\u01a2\3\2\2\2\u009b\u01a4\3\2\2\2\u009d\u01a6\3")
        buf.write("\2\2\2\u009f\u01a9\3\2\2\2\u00a1\u01ac\3\2\2\2\u00a3\u01af")
        buf.write("\3\2\2\2\u00a5\u01b1\3\2\2\2\u00a7\u01b3\3\2\2\2\u00a9")
        buf.write("\u01b5\3\2\2\2\u00ab\u01b7\3\2\2\2\u00ad\u01b9\3\2\2\2")
        buf.write("\u00af\u01bb\3\2\2\2\u00b1\u01bd\3\2\2\2\u00b3\u01bf\3")
        buf.write("\2\2\2\u00b5\u01c1\3\2\2\2\u00b7\u01c3\3\2\2\2\u00b9\u01c5")
        buf.write("\3\2\2\2\u00bb\u01c8\3\2\2\2\u00bd\u01e8\3\2\2\2\u00bf")
        buf.write("\u01ea\3\2\2\2\u00c1\u01ec\3\2\2\2\u00c3\u01ee\3\2\2\2")
        buf.write("\u00c5\u01f2\3\2\2\2\u00c7\u01fd\3\2\2\2\u00c9\u0204\3")
        buf.write("\2\2\2\u00cb\u020a\3\2\2\2\u00cd\u00ce\7b\2\2\u00ce\u00cf")
        buf.write("\7b\2\2\u00cf\u00d0\7b\2\2\u00d0\u00d4\3\2\2\2\u00d1\u00d3")
        buf.write("\13\2\2\2\u00d2\u00d1\3\2\2\2\u00d3\u00d6\3\2\2\2\u00d4")
        buf.write("\u00d5\3\2\2\2\u00d4\u00d2\3\2\2\2\u00d5\u00d7\3\2\2\2")
        buf.write("\u00d6\u00d4\3\2\2\2\u00d7\u00d8\7b\2\2\u00d8\u00d9\7")
        buf.write("b\2\2\u00d9\u00da\7b\2\2\u00da\u00db\3\2\2\2\u00db\u00dc")
        buf.write("\b\2\2\2\u00dc\4\3\2\2\2\u00dd\u00de\7\u5428\2\2\u00de")
        buf.write("\u00df\7\u521b\2\2\u00df\u00e0\7\u82e7\2\2\u00e0\6\3\2")
        buf.write("\2\2\u00e1\u00e2\7\u5984\2\2\u00e2\u00e3\7\u679e\2\2\u00e3")
        buf.write("\b\3\2\2\2\u00e4\u00e5\7\u90a5\2\2\u00e5\u00e6\7\u4e4a")
        buf.write("\2\2\u00e6\n\3\2\2\2\u00e7\u00e8\7\u5428\2\2\u00e8\u00e9")
        buf.write("\7\u521b\2\2\u00e9\f\3\2\2\2\u00ea\u00eb\7\u7ed5\2\2\u00eb")
        buf.write("\u00ec\7\u6761\2\2\u00ec\16\3\2\2\2\u00ed\u00ee\7\u5929")
        buf.write("\2\2\u00ee\u00ef\7\u4e90\2\2\u00ef\u00f0\7\u7b4b\2\2\u00f0")
        buf.write("\u00f1\7\u4e90\2\2\u00f1\20\3\2\2\2\u00f2\u00f3\7\u5c11")
        buf.write("\2\2\u00f3\u00f4\7\u4e90\2\2\u00f4\u00f5\7\u7b4b\2\2\u00f5")
        buf.write("\u00f6\7\u4e90\2\2\u00f6\22\3\2\2\2\u00f7\u00f8\7\u4e0f")
        buf.write("\2\2\u00f8\u00f9\7\u7b4b\2\2\u00f9\u00fa\7\u4e90\2\2\u00fa")
        buf.write("\24\3\2\2\2\u00fb\u00fc\7\u5929\2\2\u00fc\u00fd\7\u4e90")
        buf.write("\2\2\u00fd\26\3\2\2\2\u00fe\u00ff\7\u5c11\2\2\u00ff\u0100")
        buf.write("\7\u4e90\2\2\u0100\30\3\2\2\2\u0101\u0102\7\u5b9c\2\2")
        buf.write("\u0102\u0103\7\u4e4b\2\2\u0103\32\3\2\2\2\u0104\u0105")
        buf.write("\7\u7b4b\2\2\u0105\u0106\7\u4e90\2\2\u0106\34\3\2\2\2")
        buf.write("\u0107\u0108\7\u6bb7\2\2\u0108\36\3\2\2\2\u0109\u010a")
        buf.write("\7\u7c7d\2\2\u010a \3\2\2\2\u010b\u010c\7\u63a7\2\2\u010c")
        buf.write("\u010d\7\u53e5\2\2\u010d\"\3\2\2\2\u010e\u010f\7\u65b2")
        buf.write("\2\2\u010f$\3\2\2\2\u0110\u0111\7\u6572\2\2\u0111\u0112")
        buf.write("\7\u6370\2\2\u0112\u0113\7\u7c7d\2\2\u0113\u0114\7\u578d")
        buf.write("\2\2\u0114&\3\2\2\2\u0115\u0116\7\u951b\2\2\u0116\u0117")
        buf.write("\7\u8bf1\2\2\u0117(\3\2\2\2\u0118\u0119\7\u5e3a\2\2\u0119")
        buf.write("\u011a\7\u91d1\2\2\u011a*\3\2\2\2\u011b\u011c\7\u7c7d")
        buf.write("\2\2\u011c\u011d\7\u578d\2\2\u011d,\3\2\2\2\u011e\u011f")
        buf.write("\7\u5bfe\2\2\u011f\u0120\7\u51fc\2\2\u0120.\3\2\2\2\u0121")
        buf.write("\u0122\7\u5bfe\2\2\u0122\u0123\7\u5167\2\2\u0123\60\3")
        buf.write("\2\2\2\u0124\u0125\7\u4ed0\2\2\u0125\62\3\2\2\2\u0126")
        buf.write("\u0127\7\u904f\2\2\u0127\u0128\7\u5388\2\2\u0128\64\3")
        buf.write("\2\2\2\u0129\u012a\7\u5f55\2\2\u012a\66\3\2\2\2\u012b")
        buf.write("\u012c\7\u8df5\2\2\u012c\u012d\7\u51fc\2\2\u012d8\3\2")
        buf.write("\2\2\u012e\u012f\7\u8df5\2\2\u012f\u0130\7\u8fc9\2\2\u0130")
        buf.write(":\3\2\2\2\u0131\u0132\7\u5c1f\2\2\u0132\u0133\7\u8bd7")
        buf.write("\2\2\u0133<\3\2\2\2\u0134\u0135\7\u6357\2\2\u0135\u0136")
        buf.write("\7\u83b9\2\2\u0136>\3\2\2\2\u0137\u0138\7\u629d\2\2\u0138")
        buf.write("\u0139\7\u51fc\2\2\u0139@\3\2\2\2\u013a\u013b\7\u8fd6")
        buf.write("\2\2\u013b\u013c\7\u56e0\2\2\u013cB\3\2\2\2\u013d\u013e")
        buf.write("\7\u6255\2\2\u013e\u013f\7\u5372\2\2\u013fD\3\2\2\2\u0140")
        buf.write("\u0141\7\u8f95\2\2\u0141\u0142\7\u51fc\2\2\u0142F\3\2")
        buf.write("\2\2\u0143\u0144\7\u8f95\2\2\u0144\u0145\7\u5167\2\2\u0145")
        buf.write("H\3\2\2\2\u0146\u0147\7\u7ee9\2\2\u0147\u0148\7\u6281")
        buf.write("\2\2\u0148J\3\2\2\2\u0149\u014a\7\u4f81\2\2\u014a\u014b")
        buf.write("\7\u752a\2\2\u014bL\3\2\2\2\u014c\u014d\7\u7238\2\2\u014d")
        buf.write("N\3\2\2\2\u014e\u014f\7\u81ec\2\2\u014f\u0150\7\u6213")
        buf.write("\2\2\u0150P\3\2\2\2\u0151\u0152\7\u65bb\2\2\u0152\u0153")
        buf.write("\7\u6cd7\2\2\u0153R\3\2\2\2\u0154\u0155\7\u4e16\2\2\u0155")
        buf.write("T\3\2\2\2\u0156\u0157\7\u6218\2\2\u0157V\3\2\2\2\u0158")
        buf.write("\u0159\7\u9760\2\2\u0159X\3\2\2\2\u015a\u015b\7\u52a2")
        buf.write("\2\2\u015bZ\3\2\2\2\u015c\u015d\7\u51d1\2\2\u015d\\\3")
        buf.write("\2\2\2\u015e\u015f\7\u4e5a\2\2\u015f^\3\2\2\2\u0160\u0161")
        buf.write("\7\u9666\2\2\u0161`\3\2\2\2\u0162\u0163\7\u6a23\2\2\u0163")
        buf.write("b\3\2\2\2\u0164\u0165\7\u5e44\2\2\u0165d\3\2\2\2\u0166")
        buf.write("\u0167\7\u5e78\2\2\u0167f\3\2\2\2\u0168\u0169\7\u4e4d")
        buf.write("\2\2\u0169h\3\2\2\2\u016a\u016b\7\u7686\2\2\u016bj\3\2")
        buf.write("\2\2\u016c\u016d\7\u7721\2\2\u016dl\3\2\2\2\u016e\u016f")
        buf.write("\7\u5049\2\2\u016fn\3\2\2\2\u0170\u0171\7\u7a7c\2\2\u0171")
        buf.write("p\3\2\2\2\u0172\u0173\7\u6572\2\2\u0173r\3\2\2\2\u0174")
        buf.write("\u0175\7\u6576\2\2\u0175\u0176\7\u6572\2\2\u0176t\3\2")
        buf.write("\2\2\u0177\u0178\7\u6d70\2\2\u0178\u0179\7\u6572\2\2\u0179")
        buf.write("v\3\2\2\2\u017a\u017b\7\u4e34\2\2\u017bx\3\2\2\2\u017c")
        buf.write("\u017d\7\u5219\2\2\u017dz\3\2\2\2\u017e\u017f\7\u517a")
        buf.write("\2\2\u017f|\3\2\2\2\u0180\u0181\7\u96c8\2\2\u0181~\3\2")
        buf.write("\2\2\u0182\u0183\7\u5e05\2\2\u0183\u0184\7\u5c16\2\2\u0184")
        buf.write("\u0080\3\2\2\2\u0185\u0186\7\u4efd\2\2\u0186\u0187\7\u6111")
        buf.write("\2\2\u0187\u0082\3\2\2\2\u0188\u0189\7`\2\2\u0189\u0084")
        buf.write("\3\2\2\2\u018a\u018b\7\'\2\2\u018b\u0086\3\2\2\2\u018c")
        buf.write("\u018d\7,\2\2\u018d\u0088\3\2\2\2\u018e\u018f\7\61\2\2")
        buf.write("\u018f\u008a\3\2\2\2\u0190\u0191\7-\2\2\u0191\u008c\3")
        buf.write("\2\2\2\u0192\u0193\7/\2\2\u0193\u008e\3\2\2\2\u0194\u0195")
        buf.write("\7?\2\2\u0195\u0196\7?\2\2\u0196\u0090\3\2\2\2\u0197\u0198")
        buf.write("\7#\2\2\u0198\u0199\7?\2\2\u0199\u0092\3\2\2\2\u019a\u019b")
        buf.write("\7@\2\2\u019b\u019c\7?\2\2\u019c\u0094\3\2\2\2\u019d\u019e")
        buf.write("\7>\2\2\u019e\u019f\7?\2\2\u019f\u0096\3\2\2\2\u01a0\u01a1")
        buf.write("\7@\2\2\u01a1\u0098\3\2\2\2\u01a2\u01a3\7>\2\2\u01a3\u009a")
        buf.write("\3\2\2\2\u01a4\u01a5\7#\2\2\u01a5\u009c\3\2\2\2\u01a6")
        buf.write("\u01a7\7(\2\2\u01a7\u01a8\7(\2\2\u01a8\u009e\3\2\2\2\u01a9")
        buf.write("\u01aa\7~\2\2\u01aa\u01ab\7~\2\2\u01ab\u00a0\3\2\2\2\u01ac")
        buf.write("\u01ad\7/\2\2\u01ad\u01ae\7@\2\2\u01ae\u00a2\3\2\2\2\u01af")
        buf.write("\u01b0\t\2\2\2\u01b0\u00a4\3\2\2\2\u01b1\u01b2\t\3\2\2")
        buf.write("\u01b2\u00a6\3\2\2\2\u01b3\u01b4\t\4\2\2\u01b4\u00a8\3")
        buf.write("\2\2\2\u01b5\u01b6\t\5\2\2\u01b6\u00aa\3\2\2\2\u01b7\u01b8")
        buf.write("\t\6\2\2\u01b8\u00ac\3\2\2\2\u01b9\u01ba\7\u3003\2\2\u01ba")
        buf.write("\u00ae\3\2\2\2\u01bb\u01bc\t\7\2\2\u01bc\u00b0\3\2\2\2")
        buf.write("\u01bd\u01be\t\b\2\2\u01be\u00b2\3\2\2\2\u01bf\u01c0\t")
        buf.write("\t\2\2\u01c0\u00b4\3\2\2\2\u01c1\u01c2\t\n\2\2\u01c2\u00b6")
        buf.write("\3\2\2\2\u01c3\u01c4\7\u300c\2\2\u01c4\u00b8\3\2\2\2\u01c5")
        buf.write("\u01c6\7\u300d\2\2\u01c6\u00ba\3\2\2\2\u01c7\u01c9\t\13")
        buf.write("\2\2\u01c8\u01c7\3\2\2\2\u01c9\u01ca\3\2\2\2\u01ca\u01c8")
        buf.write("\3\2\2\2\u01ca\u01cb\3\2\2\2\u01cb\u01d2\3\2\2\2\u01cc")
        buf.write("\u01ce\7\60\2\2\u01cd\u01cf\t\13\2\2\u01ce\u01cd\3\2\2")
        buf.write("\2\u01cf\u01d0\3\2\2\2\u01d0\u01ce\3\2\2\2\u01d0\u01d1")
        buf.write("\3\2\2\2\u01d1\u01d3\3\2\2\2\u01d2\u01cc\3\2\2\2\u01d2")
        buf.write("\u01d3\3\2\2\2\u01d3\u00bc\3\2\2\2\u01d4\u01da\7$\2\2")
        buf.write("\u01d5\u01d6\7^\2\2\u01d6\u01d9\13\2\2\2\u01d7\u01d9\n")
        buf.write("\f\2\2\u01d8\u01d5\3\2\2\2\u01d8\u01d7\3\2\2\2\u01d9\u01dc")
        buf.write("\3\2\2\2\u01da\u01d8\3\2\2\2\u01da\u01db\3\2\2\2\u01db")
        buf.write("\u01dd\3\2\2\2\u01dc\u01da\3\2\2\2\u01dd\u01e9\7$\2\2")
        buf.write("\u01de\u01e4\7)\2\2\u01df\u01e0\7^\2\2\u01e0\u01e3\13")
        buf.write("\2\2\2\u01e1\u01e3\n\r\2\2\u01e2\u01df\3\2\2\2\u01e2\u01e1")
        buf.write("\3\2\2\2\u01e3\u01e6\3\2\2\2\u01e4\u01e2\3\2\2\2\u01e4")
        buf.write("\u01e5\3\2\2\2\u01e5\u01e7\3\2\2\2\u01e6\u01e4\3\2\2\2")
        buf.write("\u01e7\u01e9\7)\2\2\u01e8\u01d4\3\2\2\2\u01e8\u01de\3")
        buf.write("\2\2\2\u01e9\u00be\3\2\2\2\u01ea\u01eb\t\16\2\2\u01eb")
        buf.write("\u00c0\3\2\2\2\u01ec\u01ed\t\17\2\2\u01ed\u00c2\3\2\2")
        buf.write("\2\u01ee\u01ef\t\13\2\2\u01ef\u00c4\3\2\2\2\u01f0\u01f3")
        buf.write("\5\u00bf`\2\u01f1\u01f3\5\u00c1a\2\u01f2\u01f0\3\2\2\2")
        buf.write("\u01f2\u01f1\3\2\2\2\u01f3\u01f9\3\2\2\2\u01f4\u01f8\5")
        buf.write("\u00bf`\2\u01f5\u01f8\5\u00c1a\2\u01f6\u01f8\5\u00c3b")
        buf.write("\2\u01f7\u01f4\3\2\2\2\u01f7\u01f5\3\2\2\2\u01f7\u01f6")
        buf.write("\3\2\2\2\u01f8\u01fb\3\2\2\2\u01f9\u01f7\3\2\2\2\u01f9")
        buf.write("\u01fa\3\2\2\2\u01fa\u00c6\3\2\2\2\u01fb\u01f9\3\2\2\2")
        buf.write("\u01fc\u01fe\7\17\2\2\u01fd\u01fc\3\2\2\2\u01fd\u01fe")
        buf.write("\3\2\2\2\u01fe\u01ff\3\2\2\2\u01ff\u0200\7\f\2\2\u0200")
        buf.write("\u0201\3\2\2\2\u0201\u0202\bd\2\2\u0202\u00c8\3\2\2\2")
        buf.write("\u0203\u0205\t\20\2\2\u0204\u0203\3\2\2\2\u0205\u0206")
        buf.write("\3\2\2\2\u0206\u0204\3\2\2\2\u0206\u0207\3\2\2\2\u0207")
        buf.write("\u0208\3\2\2\2\u0208\u0209\be\2\2\u0209\u00ca\3\2\2\2")
        buf.write("\u020a\u020b\13\2\2\2\u020b\u00cc\3\2\2\2\21\2\u00d4\u01ca")
        buf.write("\u01d0\u01d2\u01d8\u01da\u01e2\u01e4\u01e8\u01f2\u01f7")
        buf.write("\u01f9\u01fd\u0206\3\b\2\2")
        return buf.getvalue()


class DuanLangLexer(Lexer):

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    COMMENT_START = 1
    K_ELSE_IF = 2
    K_IF = 3
    K_THEN = 4
    K_ELSE = 5
    K_END = 6
    K_GE = 7
    K_LE = 8
    K_NE = 9
    K_GT = 10
    K_LT = 11
    K_DEFINE = 12
    K_EQUAL = 13
    K_SEGMENT = 14
    K_CLASS = 15
    K_INTERFACE = 16
    K_NEW = 17
    K_DATA_TYPE = 18
    K_ERROR_TYPE = 19
    K_CONST = 20
    K_TYPE = 21
    K_EXPORT = 22
    K_IMPORT = 23
    K_FROM = 24
    K_FOREACH = 25
    K_WHILE = 26
    K_BREAK = 27
    K_CONTINUE = 28
    K_TRY = 29
    K_CATCH = 30
    K_THROW = 31
    K_RETURN = 32
    K_PRINT = 33
    K_OUTPUT = 34
    K_INPUT = 35
    K_INHERIT = 36
    K_USE = 37
    K_PARENT = 38
    K_SELF = 39
    K_METHOD = 40
    K_AND = 41
    K_OR = 42
    K_NOT = 43
    K_PLUS = 44
    K_MINUS = 45
    K_MULTIPLY = 46
    K_DIVIDE = 47
    K_MOD = 48
    K_POW = 49
    K_AND_WORD = 50
    K_OF = 51
    K_DE = 52
    K_TRUE = 53
    K_FALSE = 54
    K_NULL = 55
    T_NUMBER = 56
    T_INT = 57
    T_FLOAT = 58
    T_STRING = 59
    T_LIST = 60
    T_DICT = 61
    T_SET = 62
    T_BOOL = 63
    T_ANY = 64
    POW = 65
    MODULO = 66
    MULTIPLY = 67
    DIVIDE = 68
    PLUS = 69
    MINUS = 70
    EQ = 71
    NE = 72
    GE = 73
    LE = 74
    GT = 75
    LT = 76
    NOT = 77
    AND = 78
    OR = 79
    PIPE = 80
    PATH_SEP = 81
    DOT = 82
    COMMA = 83
    COLON = 84
    SEMICOLON = 85
    PAUSE = 86
    LPAREN = 87
    RPAREN = 88
    LBRACKET = 89
    RBRACKET = 90
    BOOK_L = 91
    BOOK_R = 92
    NUMBER = 93
    STRING = 94
    ID = 95
    NEWLINE = 96
    WS = 97
    UNKNOWN = 98

    channelNames = [ u"DEFAULT_TOKEN_CHANNEL", u"HIDDEN" ]

    modeNames = [ "DEFAULT_MODE" ]

    literalNames = [ "<INVALID>",
            "'\u5426\u5219\u82E5'", "'\u5982\u679C'", "'\u90A3\u4E48'", 
            "'\u5426\u5219'", "'\u7ED3\u675F'", "'\u5927\u4E8E\u7B49\u4E8E'", 
            "'\u5C0F\u4E8E\u7B49\u4E8E'", "'\u4E0D\u7B49\u4E8E'", "'\u5927\u4E8E'", 
            "'\u5C0F\u4E8E'", "'\u5B9A\u4E49'", "'\u7B49\u4E8E'", "'\u6BB5'", 
            "'\u7C7B'", "'\u63A5\u53E3'", "'\u65B0'", "'\u6570\u636E\u7C7B\u578B'", 
            "'\u9519\u8BEF'", "'\u5E38\u91CF'", "'\u7C7B\u578B'", "'\u5BFC\u51FA'", 
            "'\u5BFC\u5165'", "'\u4ECE'", "'\u904D\u5386'", "'\u5F53'", 
            "'\u8DF3\u51FA'", "'\u8DF3\u8FC7'", "'\u5C1D\u8BD5'", "'\u6355\u83B7'", 
            "'\u629B\u51FA'", "'\u8FD4\u56DE'", "'\u6253\u5370'", "'\u8F93\u51FA'", 
            "'\u8F93\u5165'", "'\u7EE7\u627F'", "'\u4F7F\u7528'", "'\u7236'", 
            "'\u81EA\u6211'", "'\u65B9\u6CD5'", "'\u4E14'", "'\u6216'", 
            "'\u975E'", "'\u52A0'", "'\u51CF'", "'\u4E58'", "'\u9664'", 
            "'\u6A21'", "'\u5E42'", "'\u5E76'", "'\u4E4B'", "'\u7684'", 
            "'\u771F'", "'\u5047'", "'\u7A7A'", "'\u6570'", "'\u6574\u6570'", 
            "'\u6D6E\u6570'", "'\u4E32'", "'\u5217'", "'\u5178'", "'\u96C6'", 
            "'\u5E03\u5C14'", "'\u4EFB\u610F'", "'^'", "'%'", "'*'", "'/'", 
            "'+'", "'-'", "'=='", "'!='", "'>='", "'<='", "'>'", "'<'", 
            "'!'", "'&&'", "'||'", "'->'", "'\u3001'", "'\u300A'", "'\u300B'" ]

    symbolicNames = [ "<INVALID>",
            "COMMENT_START", "K_ELSE_IF", "K_IF", "K_THEN", "K_ELSE", "K_END", 
            "K_GE", "K_LE", "K_NE", "K_GT", "K_LT", "K_DEFINE", "K_EQUAL", 
            "K_SEGMENT", "K_CLASS", "K_INTERFACE", "K_NEW", "K_DATA_TYPE", 
            "K_ERROR_TYPE", "K_CONST", "K_TYPE", "K_EXPORT", "K_IMPORT", 
            "K_FROM", "K_FOREACH", "K_WHILE", "K_BREAK", "K_CONTINUE", "K_TRY", 
            "K_CATCH", "K_THROW", "K_RETURN", "K_PRINT", "K_OUTPUT", "K_INPUT", 
            "K_INHERIT", "K_USE", "K_PARENT", "K_SELF", "K_METHOD", "K_AND", 
            "K_OR", "K_NOT", "K_PLUS", "K_MINUS", "K_MULTIPLY", "K_DIVIDE", 
            "K_MOD", "K_POW", "K_AND_WORD", "K_OF", "K_DE", "K_TRUE", "K_FALSE", 
            "K_NULL", "T_NUMBER", "T_INT", "T_FLOAT", "T_STRING", "T_LIST", 
            "T_DICT", "T_SET", "T_BOOL", "T_ANY", "POW", "MODULO", "MULTIPLY", 
            "DIVIDE", "PLUS", "MINUS", "EQ", "NE", "GE", "LE", "GT", "LT", 
            "NOT", "AND", "OR", "PIPE", "PATH_SEP", "DOT", "COMMA", "COLON", 
            "SEMICOLON", "PAUSE", "LPAREN", "RPAREN", "LBRACKET", "RBRACKET", 
            "BOOK_L", "BOOK_R", "NUMBER", "STRING", "ID", "NEWLINE", "WS", 
            "UNKNOWN" ]

    ruleNames = [ "COMMENT_START", "K_ELSE_IF", "K_IF", "K_THEN", "K_ELSE", 
                  "K_END", "K_GE", "K_LE", "K_NE", "K_GT", "K_LT", "K_DEFINE", 
                  "K_EQUAL", "K_SEGMENT", "K_CLASS", "K_INTERFACE", "K_NEW", 
                  "K_DATA_TYPE", "K_ERROR_TYPE", "K_CONST", "K_TYPE", "K_EXPORT", 
                  "K_IMPORT", "K_FROM", "K_FOREACH", "K_WHILE", "K_BREAK", 
                  "K_CONTINUE", "K_TRY", "K_CATCH", "K_THROW", "K_RETURN", 
                  "K_PRINT", "K_OUTPUT", "K_INPUT", "K_INHERIT", "K_USE", 
                  "K_PARENT", "K_SELF", "K_METHOD", "K_AND", "K_OR", "K_NOT", 
                  "K_PLUS", "K_MINUS", "K_MULTIPLY", "K_DIVIDE", "K_MOD", 
                  "K_POW", "K_AND_WORD", "K_OF", "K_DE", "K_TRUE", "K_FALSE", 
                  "K_NULL", "T_NUMBER", "T_INT", "T_FLOAT", "T_STRING", 
                  "T_LIST", "T_DICT", "T_SET", "T_BOOL", "T_ANY", "POW", 
                  "MODULO", "MULTIPLY", "DIVIDE", "PLUS", "MINUS", "EQ", 
                  "NE", "GE", "LE", "GT", "LT", "NOT", "AND", "OR", "PIPE", 
                  "PATH_SEP", "DOT", "COMMA", "COLON", "SEMICOLON", "PAUSE", 
                  "LPAREN", "RPAREN", "LBRACKET", "RBRACKET", "BOOK_L", 
                  "BOOK_R", "NUMBER", "STRING", "IDEOGRAPHIC", "LETTER", 
                  "DIGIT", "ID", "NEWLINE", "WS", "UNKNOWN" ]

    grammarFileName = "DuanLang.g4"

    def __init__(self, input=None, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.9.2")
        self._interp = LexerATNSimulator(self, self.atn, self.decisionsToDFA, PredictionContextCache())
        self._actions = None
        self._predicates = None


    def format_error_msg(self, msg: str) -> str:
        return f"[段言语法错误] 行{self._ctx.start.line}: {msg}"


