# Generated from g:\dumategithub\duan\antlrparser\DuanLang.g4 by ANTLR 4.9.2
# encoding: utf-8
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
        buf.write("\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\3d")
        buf.write("\u02c8\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7\t\7")
        buf.write("\4\b\t\b\4\t\t\t\4\n\t\n\4\13\t\13\4\f\t\f\4\r\t\r\4\16")
        buf.write("\t\16\4\17\t\17\4\20\t\20\4\21\t\21\4\22\t\22\4\23\t\23")
        buf.write("\4\24\t\24\4\25\t\25\4\26\t\26\4\27\t\27\4\30\t\30\4\31")
        buf.write("\t\31\4\32\t\32\4\33\t\33\4\34\t\34\4\35\t\35\4\36\t\36")
        buf.write("\4\37\t\37\4 \t \4!\t!\4\"\t\"\4#\t#\4$\t$\4%\t%\4&\t")
        buf.write("&\4\'\t\'\4(\t(\4)\t)\4*\t*\4+\t+\4,\t,\4-\t-\4.\t.\4")
        buf.write("/\t/\4\60\t\60\4\61\t\61\4\62\t\62\4\63\t\63\4\64\t\64")
        buf.write("\4\65\t\65\4\66\t\66\4\67\t\67\48\t8\49\t9\4:\t:\3\2\3")
        buf.write("\2\3\2\3\2\3\2\7\2z\n\2\f\2\16\2}\13\2\3\2\3\2\3\3\3\3")
        buf.write("\3\3\3\3\3\4\3\4\3\4\3\4\3\4\5\4\u008a\n\4\3\5\3\5\3\5")
        buf.write("\3\5\3\5\3\5\3\5\3\5\7\5\u0094\n\5\f\5\16\5\u0097\13\5")
        buf.write("\5\5\u0099\n\5\3\5\3\5\3\5\3\5\7\5\u009f\n\5\f\5\16\5")
        buf.write("\u00a2\13\5\5\5\u00a4\n\5\3\5\3\5\7\5\u00a8\n\5\f\5\16")
        buf.write("\5\u00ab\13\5\3\5\3\5\5\5\u00af\n\5\3\6\3\6\3\6\5\6\u00b4")
        buf.write("\n\6\3\7\3\7\3\7\3\7\3\7\3\7\5\7\u00bc\n\7\3\7\3\7\3\7")
        buf.write("\5\7\u00c1\n\7\3\7\3\7\3\7\3\7\5\7\u00c7\n\7\3\b\3\b\3")
        buf.write("\b\3\b\3\b\5\b\u00ce\n\b\3\b\3\b\3\b\3\b\3\b\5\b\u00d5")
        buf.write("\n\b\3\t\3\t\3\t\3\t\3\t\3\t\3\t\3\t\7\t\u00df\n\t\f\t")
        buf.write("\16\t\u00e2\13\t\5\t\u00e4\n\t\3\t\3\t\7\t\u00e8\n\t\f")
        buf.write("\t\16\t\u00eb\13\t\3\t\3\t\5\t\u00ef\n\t\3\n\3\n\5\n\u00f3")
        buf.write("\n\n\3\n\3\n\5\n\u00f7\n\n\5\n\u00f9\n\n\3\13\3\13\3\13")
        buf.write("\3\13\3\13\3\13\5\13\u0101\n\13\3\13\3\13\3\13\3\13\3")
        buf.write("\f\3\f\3\f\3\f\3\r\3\r\3\r\3\r\3\r\3\r\5\r\u0111\n\r\3")
        buf.write("\r\3\r\3\r\5\r\u0116\n\r\3\r\3\r\3\r\3\r\5\r\u011c\n\r")
        buf.write("\3\16\3\16\3\16\7\16\u0121\n\16\f\16\16\16\u0124\13\16")
        buf.write("\3\17\3\17\3\17\5\17\u0129\n\17\3\17\3\17\5\17\u012d\n")
        buf.write("\17\3\20\7\20\u0130\n\20\f\20\16\20\u0133\13\20\3\21\3")
        buf.write("\21\3\21\3\21\3\21\3\21\6\21\u013b\n\21\r\21\16\21\u013c")
        buf.write("\3\21\3\21\5\21\u0141\n\21\3\22\3\22\3\22\3\22\5\22\u0147")
        buf.write("\n\22\3\23\3\23\3\23\3\23\3\23\3\23\6\23\u014f\n\23\r")
        buf.write("\23\16\23\u0150\3\23\3\23\5\23\u0155\n\23\3\24\3\24\3")
        buf.write("\24\3\24\3\24\5\24\u015c\n\24\3\24\3\24\3\24\5\24\u0161")
        buf.write("\n\24\5\24\u0163\n\24\3\25\3\25\3\25\3\25\3\25\5\25\u016a")
        buf.write("\n\25\3\25\5\25\u016d\n\25\3\26\3\26\3\26\7\26\u0172\n")
        buf.write("\26\f\26\16\26\u0175\13\26\3\27\3\27\3\27\7\27\u017a\n")
        buf.write("\27\f\27\16\27\u017d\13\27\3\30\3\30\3\30\3\30\5\30\u0183")
        buf.write("\n\30\3\31\3\31\3\31\3\31\3\31\3\31\3\31\3\31\3\31\3\31")
        buf.write("\3\31\3\31\5\31\u0191\n\31\3\32\3\32\3\32\3\32\5\32\u0197")
        buf.write("\n\32\3\32\5\32\u019a\n\32\3\33\3\33\3\33\3\33\5\33\u01a0")
        buf.write("\n\33\3\34\3\34\3\34\3\34\3\34\5\34\u01a7\n\34\3\35\3")
        buf.write("\35\3\35\3\35\3\35\5\35\u01ae\n\35\3\35\3\35\3\35\3\35")
        buf.write("\3\35\3\35\7\35\u01b6\n\35\f\35\16\35\u01b9\13\35\3\35")
        buf.write("\3\35\3\35\5\35\u01be\n\35\3\35\3\35\5\35\u01c2\n\35\3")
        buf.write("\36\3\36\3\36\3\36\3\36\5\36\u01c9\n\36\3\36\3\36\5\36")
        buf.write("\u01cd\n\36\3\37\3\37\3\37\3\37\3\37\3\37\3\37\3\37\3")
        buf.write("\37\5\37\u01d8\n\37\3 \3 \3 \3 \5 \u01de\n \3 \3 \5 \u01e2")
        buf.write("\n \3!\3!\5!\u01e6\n!\3!\5!\u01e9\n!\3\"\3\"\5\"\u01ed")
        buf.write("\n\"\3#\3#\5#\u01f1\n#\3$\3$\3$\3$\3$\3$\3$\3$\3$\5$\u01fc")
        buf.write("\n$\3%\3%\3%\5%\u0201\n%\3&\3&\3&\5&\u0206\n&\3\'\3\'")
        buf.write("\5\'\u020a\n\'\3(\3(\3)\3)\3)\7)\u0211\n)\f)\16)\u0214")
        buf.write("\13)\3*\3*\3*\7*\u0219\n*\f*\16*\u021c\13*\3+\3+\3+\7")
        buf.write("+\u0221\n+\f+\16+\u0224\13+\3,\3,\3,\3,\7,\u022a\n,\f")
        buf.write(",\16,\u022d\13,\3-\3-\3.\3.\3.\3.\7.\u0235\n.\f.\16.\u0238")
        buf.write("\13.\3/\3/\3\60\3\60\3\60\3\60\7\60\u0240\n\60\f\60\16")
        buf.write("\60\u0243\13\60\3\61\3\61\3\62\3\62\3\62\3\62\3\62\5\62")
        buf.write("\u024c\n\62\3\63\3\63\3\63\3\63\3\63\3\63\5\63\u0254\n")
        buf.write("\63\3\63\3\63\3\63\5\63\u0259\n\63\3\63\3\63\3\63\3\63")
        buf.write("\3\63\3\63\3\63\7\63\u0262\n\63\f\63\16\63\u0265\13\63")
        buf.write("\3\64\3\64\3\64\3\64\3\64\3\64\3\64\3\64\3\64\3\64\3\64")
        buf.write("\3\64\3\64\3\64\3\64\3\64\5\64\u0277\n\64\3\64\3\64\3")
        buf.write("\64\3\64\3\64\3\64\3\64\3\64\5\64\u0281\n\64\3\64\5\64")
        buf.write("\u0284\n\64\3\65\3\65\3\65\7\65\u0289\n\65\f\65\16\65")
        buf.write("\u028c\13\65\3\66\3\66\3\66\3\66\3\67\3\67\3\67\5\67\u0295")
        buf.write("\n\67\38\38\38\38\38\78\u029c\n8\f8\168\u029f\138\38\3")
        buf.write("8\39\39\39\39\39\39\39\39\39\39\39\39\39\39\39\39\39\3")
        buf.write("9\39\39\39\39\39\39\39\39\39\59\u02be\n9\3:\3:\3:\7:\u02c3")
        buf.write("\n:\f:\16:\u02c6\13:\3:\2\2;\2\4\6\b\n\f\16\20\22\24\26")
        buf.write("\30\32\34\36 \"$&(*,.\60\62\64\668:<>@BDFHJLNPRTVXZ\\")
        buf.write("^`bdfhjlnpr\2\t\3\2#$\4\2\64\64RR\5\2\t\r\17\17IN\4\2")
        buf.write("./GH\4\2\60\63CF\4\2--OO\4\2//HH\2\u030c\2{\3\2\2\2\4")
        buf.write("\u0080\3\2\2\2\6\u0089\3\2\2\2\b\u008b\3\2\2\2\n\u00b3")
        buf.write("\3\2\2\2\f\u00b5\3\2\2\2\16\u00c8\3\2\2\2\20\u00d6\3\2")
        buf.write("\2\2\22\u00f8\3\2\2\2\24\u00fa\3\2\2\2\26\u0106\3\2\2")
        buf.write("\2\30\u010a\3\2\2\2\32\u011d\3\2\2\2\34\u0125\3\2\2\2")
        buf.write("\36\u0131\3\2\2\2 \u0134\3\2\2\2\"\u0142\3\2\2\2$\u0148")
        buf.write("\3\2\2\2&\u0162\3\2\2\2(\u0164\3\2\2\2*\u016e\3\2\2\2")
        buf.write(",\u0176\3\2\2\2.\u0182\3\2\2\2\60\u0190\3\2\2\2\62\u0192")
        buf.write("\3\2\2\2\64\u019b\3\2\2\2\66\u01a6\3\2\2\28\u01a8\3\2")
        buf.write("\2\2:\u01c3\3\2\2\2<\u01d7\3\2\2\2>\u01d9\3\2\2\2@\u01e3")
        buf.write("\3\2\2\2B\u01ea\3\2\2\2D\u01ee\3\2\2\2F\u01f2\3\2\2\2")
        buf.write("H\u01fd\3\2\2\2J\u0202\3\2\2\2L\u0207\3\2\2\2N\u020b\3")
        buf.write("\2\2\2P\u020d\3\2\2\2R\u0215\3\2\2\2T\u021d\3\2\2\2V\u0225")
        buf.write("\3\2\2\2X\u022e\3\2\2\2Z\u0230\3\2\2\2\\\u0239\3\2\2\2")
        buf.write("^\u023b\3\2\2\2`\u0244\3\2\2\2b\u024b\3\2\2\2d\u024d\3")
        buf.write("\2\2\2f\u0283\3\2\2\2h\u0285\3\2\2\2j\u028d\3\2\2\2l\u0294")
        buf.write("\3\2\2\2n\u0296\3\2\2\2p\u02bd\3\2\2\2r\u02bf\3\2\2\2")
        buf.write("tz\5\4\3\2uz\5&\24\2vz\5(\25\2wz\5\6\4\2xz\5\60\31\2y")
        buf.write("t\3\2\2\2yu\3\2\2\2yv\3\2\2\2yw\3\2\2\2yx\3\2\2\2z}\3")
        buf.write("\2\2\2{y\3\2\2\2{|\3\2\2\2|~\3\2\2\2}{\3\2\2\2~\177\7")
        buf.write("\2\2\3\177\3\3\2\2\2\u0080\u0081\7[\2\2\u0081\u0082\7")
        buf.write("a\2\2\u0082\u0083\7\\\2\2\u0083\5\3\2\2\2\u0084\u008a")
        buf.write("\5\30\r\2\u0085\u008a\5\b\5\2\u0086\u008a\5\20\t\2\u0087")
        buf.write("\u008a\5 \21\2\u0088\u008a\5$\23\2\u0089\u0084\3\2\2\2")
        buf.write("\u0089\u0085\3\2\2\2\u0089\u0086\3\2\2\2\u0089\u0087\3")
        buf.write("\2\2\2\u0089\u0088\3\2\2\2\u008a\7\3\2\2\2\u008b\u008c")
        buf.write("\7]\2\2\u008c\u008d\7a\2\2\u008d\u008e\7^\2\2\u008e\u0098")
        buf.write("\7\21\2\2\u008f\u0090\7&\2\2\u0090\u0095\5l\67\2\u0091")
        buf.write("\u0092\7U\2\2\u0092\u0094\5l\67\2\u0093\u0091\3\2\2\2")
        buf.write("\u0094\u0097\3\2\2\2\u0095\u0093\3\2\2\2\u0095\u0096\3")
        buf.write("\2\2\2\u0096\u0099\3\2\2\2\u0097\u0095\3\2\2\2\u0098\u008f")
        buf.write("\3\2\2\2\u0098\u0099\3\2\2\2\u0099\u00a3\3\2\2\2\u009a")
        buf.write("\u009b\7\'\2\2\u009b\u00a0\5l\67\2\u009c\u009d\7U\2\2")
        buf.write("\u009d\u009f\5l\67\2\u009e\u009c\3\2\2\2\u009f\u00a2\3")
        buf.write("\2\2\2\u00a0\u009e\3\2\2\2\u00a0\u00a1\3\2\2\2\u00a1\u00a4")
        buf.write("\3\2\2\2\u00a2\u00a0\3\2\2\2\u00a3\u009a\3\2\2\2\u00a3")
        buf.write("\u00a4\3\2\2\2\u00a4\u00a5\3\2\2\2\u00a5\u00a9\7V\2\2")
        buf.write("\u00a6\u00a8\5\n\6\2\u00a7\u00a6\3\2\2\2\u00a8\u00ab\3")
        buf.write("\2\2\2\u00a9\u00a7\3\2\2\2\u00a9\u00aa\3\2\2\2\u00aa\u00ac")
        buf.write("\3\2\2\2\u00ab\u00a9\3\2\2\2\u00ac\u00ae\7\b\2\2\u00ad")
        buf.write("\u00af\7T\2\2\u00ae\u00ad\3\2\2\2\u00ae\u00af\3\2\2\2")
        buf.write("\u00af\t\3\2\2\2\u00b0\u00b4\5\62\32\2\u00b1\u00b4\5\f")
        buf.write("\7\2\u00b2\u00b4\5\16\b\2\u00b3\u00b0\3\2\2\2\u00b3\u00b1")
        buf.write("\3\2\2\2\u00b3\u00b2\3\2\2\2\u00b4\13\3\2\2\2\u00b5\u00b6")
        buf.write("\7]\2\2\u00b6\u00b7\7a\2\2\u00b7\u00b8\7^\2\2\u00b8\u00b9")
        buf.write("\7*\2\2\u00b9\u00bb\7Y\2\2\u00ba\u00bc\5\32\16\2\u00bb")
        buf.write("\u00ba\3\2\2\2\u00bb\u00bc\3\2\2\2\u00bc\u00bd\3\2\2\2")
        buf.write("\u00bd\u00c0\7Z\2\2\u00be\u00bf\7R\2\2\u00bf\u00c1\5l")
        buf.write("\67\2\u00c0\u00be\3\2\2\2\u00c0\u00c1\3\2\2\2\u00c1\u00c2")
        buf.write("\3\2\2\2\u00c2\u00c3\7V\2\2\u00c3\u00c4\5\36\20\2\u00c4")
        buf.write("\u00c6\7\b\2\2\u00c5\u00c7\7T\2\2\u00c6\u00c5\3\2\2\2")
        buf.write("\u00c6\u00c7\3\2\2\2\u00c7\r\3\2\2\2\u00c8\u00c9\7]\2")
        buf.write("\2\u00c9\u00ca\7a\2\2\u00ca\u00cb\7^\2\2\u00cb\u00cd\7")
        buf.write("Y\2\2\u00cc\u00ce\5\32\16\2\u00cd\u00cc\3\2\2\2\u00cd")
        buf.write("\u00ce\3\2\2\2\u00ce\u00cf\3\2\2\2\u00cf\u00d0\7Z\2\2")
        buf.write("\u00d0\u00d1\7V\2\2\u00d1\u00d2\5\36\20\2\u00d2\u00d4")
        buf.write("\7\b\2\2\u00d3\u00d5\7T\2\2\u00d4\u00d3\3\2\2\2\u00d4")
        buf.write("\u00d5\3\2\2\2\u00d5\17\3\2\2\2\u00d6\u00d7\7]\2\2\u00d7")
        buf.write("\u00d8\7a\2\2\u00d8\u00d9\7^\2\2\u00d9\u00e3\7\22\2\2")
        buf.write("\u00da\u00db\7&\2\2\u00db\u00e0\5l\67\2\u00dc\u00dd\7")
        buf.write("U\2\2\u00dd\u00df\5l\67\2\u00de\u00dc\3\2\2\2\u00df\u00e2")
        buf.write("\3\2\2\2\u00e0\u00de\3\2\2\2\u00e0\u00e1\3\2\2\2\u00e1")
        buf.write("\u00e4\3\2\2\2\u00e2\u00e0\3\2\2\2\u00e3\u00da\3\2\2\2")
        buf.write("\u00e3\u00e4\3\2\2\2\u00e4\u00e5\3\2\2\2\u00e5\u00e9\7")
        buf.write("V\2\2\u00e6\u00e8\5\22\n\2\u00e7\u00e6\3\2\2\2\u00e8\u00eb")
        buf.write("\3\2\2\2\u00e9\u00e7\3\2\2\2\u00e9\u00ea\3\2\2\2\u00ea")
        buf.write("\u00ec\3\2\2\2\u00eb\u00e9\3\2\2\2\u00ec\u00ee\7\b\2\2")
        buf.write("\u00ed\u00ef\7T\2\2\u00ee\u00ed\3\2\2\2\u00ee\u00ef\3")
        buf.write("\2\2\2\u00ef\21\3\2\2\2\u00f0\u00f2\5\24\13\2\u00f1\u00f3")
        buf.write("\7T\2\2\u00f2\u00f1\3\2\2\2\u00f2\u00f3\3\2\2\2\u00f3")
        buf.write("\u00f9\3\2\2\2\u00f4\u00f6\5\26\f\2\u00f5\u00f7\7T\2\2")
        buf.write("\u00f6\u00f5\3\2\2\2\u00f6\u00f7\3\2\2\2\u00f7\u00f9\3")
        buf.write("\2\2\2\u00f8\u00f0\3\2\2\2\u00f8\u00f4\3\2\2\2\u00f9\23")
        buf.write("\3\2\2\2\u00fa\u00fb\7]\2\2\u00fb\u00fc\7a\2\2\u00fc\u00fd")
        buf.write("\7^\2\2\u00fd\u00fe\7*\2\2\u00fe\u0100\7Y\2\2\u00ff\u0101")
        buf.write("\5\32\16\2\u0100\u00ff\3\2\2\2\u0100\u0101\3\2\2\2\u0101")
        buf.write("\u0102\3\2\2\2\u0102\u0103\7Z\2\2\u0103\u0104\7R\2\2\u0104")
        buf.write("\u0105\5l\67\2\u0105\25\3\2\2\2\u0106\u0107\7a\2\2\u0107")
        buf.write("\u0108\7V\2\2\u0108\u0109\5l\67\2\u0109\27\3\2\2\2\u010a")
        buf.write("\u010b\7]\2\2\u010b\u010c\7a\2\2\u010c\u010d\7^\2\2\u010d")
        buf.write("\u010e\7\20\2\2\u010e\u0110\7Y\2\2\u010f\u0111\5\32\16")
        buf.write("\2\u0110\u010f\3\2\2\2\u0110\u0111\3\2\2\2\u0111\u0112")
        buf.write("\3\2\2\2\u0112\u0115\7Z\2\2\u0113\u0114\7R\2\2\u0114\u0116")
        buf.write("\5l\67\2\u0115\u0113\3\2\2\2\u0115\u0116\3\2\2\2\u0116")
        buf.write("\u0117\3\2\2\2\u0117\u0118\7V\2\2\u0118\u0119\5\36\20")
        buf.write("\2\u0119\u011b\7\b\2\2\u011a\u011c\7T\2\2\u011b\u011a")
        buf.write("\3\2\2\2\u011b\u011c\3\2\2\2\u011c\31\3\2\2\2\u011d\u0122")
        buf.write("\5\34\17\2\u011e\u011f\7U\2\2\u011f\u0121\5\34\17\2\u0120")
        buf.write("\u011e\3\2\2\2\u0121\u0124\3\2\2\2\u0122\u0120\3\2\2\2")
        buf.write("\u0122\u0123\3\2\2\2\u0123\33\3\2\2\2\u0124\u0122\3\2")
        buf.write("\2\2\u0125\u0128\7a\2\2\u0126\u0127\7V\2\2\u0127\u0129")
        buf.write("\5l\67\2\u0128\u0126\3\2\2\2\u0128\u0129\3\2\2\2\u0129")
        buf.write("\u012c\3\2\2\2\u012a\u012b\7\17\2\2\u012b\u012d\5N(\2")
        buf.write("\u012c\u012a\3\2\2\2\u012c\u012d\3\2\2\2\u012d\35\3\2")
        buf.write("\2\2\u012e\u0130\5\60\31\2\u012f\u012e\3\2\2\2\u0130\u0133")
        buf.write("\3\2\2\2\u0131\u012f\3\2\2\2\u0131\u0132\3\2\2\2\u0132")
        buf.write("\37\3\2\2\2\u0133\u0131\3\2\2\2\u0134\u0135\7]\2\2\u0135")
        buf.write("\u0136\7a\2\2\u0136\u0137\7^\2\2\u0137\u0138\7\24\2\2")
        buf.write("\u0138\u013a\7V\2\2\u0139\u013b\5\"\22\2\u013a\u0139\3")
        buf.write("\2\2\2\u013b\u013c\3\2\2\2\u013c\u013a\3\2\2\2\u013c\u013d")
        buf.write("\3\2\2\2\u013d\u013e\3\2\2\2\u013e\u0140\7\b\2\2\u013f")
        buf.write("\u0141\7T\2\2\u0140\u013f\3\2\2\2\u0140\u0141\3\2\2\2")
        buf.write("\u0141!\3\2\2\2\u0142\u0143\7a\2\2\u0143\u0144\7V\2\2")
        buf.write("\u0144\u0146\5l\67\2\u0145\u0147\7T\2\2\u0146\u0145\3")
        buf.write("\2\2\2\u0146\u0147\3\2\2\2\u0147#\3\2\2\2\u0148\u0149")
        buf.write("\7]\2\2\u0149\u014a\7a\2\2\u014a\u014b\7^\2\2\u014b\u014c")
        buf.write("\7\25\2\2\u014c\u014e\7V\2\2\u014d\u014f\5\"\22\2\u014e")
        buf.write("\u014d\3\2\2\2\u014f\u0150\3\2\2\2\u0150\u014e\3\2\2\2")
        buf.write("\u0150\u0151\3\2\2\2\u0151\u0152\3\2\2\2\u0152\u0154\7")
        buf.write("\b\2\2\u0153\u0155\7T\2\2\u0154\u0153\3\2\2\2\u0154\u0155")
        buf.write("\3\2\2\2\u0155%\3\2\2\2\u0156\u0157\7\32\2\2\u0157\u0158")
        buf.write("\5*\26\2\u0158\u0159\7\31\2\2\u0159\u015b\5,\27\2\u015a")
        buf.write("\u015c\7T\2\2\u015b\u015a\3\2\2\2\u015b\u015c\3\2\2\2")
        buf.write("\u015c\u0163\3\2\2\2\u015d\u015e\7\31\2\2\u015e\u0160")
        buf.write("\5,\27\2\u015f\u0161\7T\2\2\u0160\u015f\3\2\2\2\u0160")
        buf.write("\u0161\3\2\2\2\u0161\u0163\3\2\2\2\u0162\u0156\3\2\2\2")
        buf.write("\u0162\u015d\3\2\2\2\u0163\'\3\2\2\2\u0164\u0169\7\30")
        buf.write("\2\2\u0165\u016a\7a\2\2\u0166\u0167\7]\2\2\u0167\u0168")
        buf.write("\7a\2\2\u0168\u016a\7^\2\2\u0169\u0165\3\2\2\2\u0169\u0166")
        buf.write("\3\2\2\2\u016a\u016c\3\2\2\2\u016b\u016d\7T\2\2\u016c")
        buf.write("\u016b\3\2\2\2\u016c\u016d\3\2\2\2\u016d)\3\2\2\2\u016e")
        buf.write("\u0173\7a\2\2\u016f\u0170\7S\2\2\u0170\u0172\7a\2\2\u0171")
        buf.write("\u016f\3\2\2\2\u0172\u0175\3\2\2\2\u0173\u0171\3\2\2\2")
        buf.write("\u0173\u0174\3\2\2\2\u0174+\3\2\2\2\u0175\u0173\3\2\2")
        buf.write("\2\u0176\u017b\5.\30\2\u0177\u0178\7U\2\2\u0178\u017a")
        buf.write("\5.\30\2\u0179\u0177\3\2\2\2\u017a\u017d\3\2\2\2\u017b")
        buf.write("\u0179\3\2\2\2\u017b\u017c\3\2\2\2\u017c-\3\2\2\2\u017d")
        buf.write("\u017b\3\2\2\2\u017e\u017f\7]\2\2\u017f\u0180\7a\2\2\u0180")
        buf.write("\u0183\7^\2\2\u0181\u0183\7a\2\2\u0182\u017e\3\2\2\2\u0182")
        buf.write("\u0181\3\2\2\2\u0183/\3\2\2\2\u0184\u0191\5\62\32\2\u0185")
        buf.write("\u0191\5\64\33\2\u0186\u0191\58\35\2\u0187\u0191\5:\36")
        buf.write("\2\u0188\u0191\5> \2\u0189\u0191\5@!\2\u018a\u0191\5B")
        buf.write("\"\2\u018b\u0191\5D#\2\u018c\u0191\5F$\2\u018d\u0191\5")
        buf.write("H%\2\u018e\u0191\5J&\2\u018f\u0191\5L\'\2\u0190\u0184")
        buf.write("\3\2\2\2\u0190\u0185\3\2\2\2\u0190\u0186\3\2\2\2\u0190")
        buf.write("\u0187\3\2\2\2\u0190\u0188\3\2\2\2\u0190\u0189\3\2\2\2")
        buf.write("\u0190\u018a\3\2\2\2\u0190\u018b\3\2\2\2\u0190\u018c\3")
        buf.write("\2\2\2\u0190\u018d\3\2\2\2\u0190\u018e\3\2\2\2\u0190\u018f")
        buf.write("\3\2\2\2\u0191\61\3\2\2\2\u0192\u0193\7\16\2\2\u0193\u0196")
        buf.write("\7a\2\2\u0194\u0195\7\17\2\2\u0195\u0197\5N(\2\u0196\u0194")
        buf.write("\3\2\2\2\u0196\u0197\3\2\2\2\u0197\u0199\3\2\2\2\u0198")
        buf.write("\u019a\7T\2\2\u0199\u0198\3\2\2\2\u0199\u019a\3\2\2\2")
        buf.write("\u019a\63\3\2\2\2\u019b\u019c\5\66\34\2\u019c\u019d\7")
        buf.write("\17\2\2\u019d\u019f\5N(\2\u019e\u01a0\7T\2\2\u019f\u019e")
        buf.write("\3\2\2\2\u019f\u01a0\3\2\2\2\u01a0\65\3\2\2\2\u01a1\u01a7")
        buf.write("\7a\2\2\u01a2\u01a3\5N(\2\u01a3\u01a4\7\65\2\2\u01a4\u01a5")
        buf.write("\7a\2\2\u01a5\u01a7\3\2\2\2\u01a6\u01a1\3\2\2\2\u01a6")
        buf.write("\u01a2\3\2\2\2\u01a7\67\3\2\2\2\u01a8\u01a9\7\5\2\2\u01a9")
        buf.write("\u01aa\5N(\2\u01aa\u01ad\7\6\2\2\u01ab\u01ac\7V\2\2\u01ac")
        buf.write("\u01ae\5\36\20\2\u01ad\u01ab\3\2\2\2\u01ad\u01ae\3\2\2")
        buf.write("\2\u01ae\u01b7\3\2\2\2\u01af\u01b0\7\4\2\2\u01b0\u01b1")
        buf.write("\5N(\2\u01b1\u01b2\7\6\2\2\u01b2\u01b3\7V\2\2\u01b3\u01b4")
        buf.write("\5\36\20\2\u01b4\u01b6\3\2\2\2\u01b5\u01af\3\2\2\2\u01b6")
        buf.write("\u01b9\3\2\2\2\u01b7\u01b5\3\2\2\2\u01b7\u01b8\3\2\2\2")
        buf.write("\u01b8\u01bd\3\2\2\2\u01b9\u01b7\3\2\2\2\u01ba\u01bb\7")
        buf.write("\7\2\2\u01bb\u01bc\7V\2\2\u01bc\u01be\5\36\20\2\u01bd")
        buf.write("\u01ba\3\2\2\2\u01bd\u01be\3\2\2\2\u01be\u01bf\3\2\2\2")
        buf.write("\u01bf\u01c1\7\b\2\2\u01c0\u01c2\7T\2\2\u01c1\u01c0\3")
        buf.write("\2\2\2\u01c1\u01c2\3\2\2\2\u01c29\3\2\2\2\u01c3\u01c4")
        buf.write("\7\33\2\2\u01c4\u01c5\5<\37\2\u01c5\u01c8\5N(\2\u01c6")
        buf.write("\u01c7\7V\2\2\u01c7\u01c9\5\36\20\2\u01c8\u01c6\3\2\2")
        buf.write("\2\u01c8\u01c9\3\2\2\2\u01c9\u01ca\3\2\2\2\u01ca\u01cc")
        buf.write("\7\b\2\2\u01cb\u01cd\7T\2\2\u01cc\u01cb\3\2\2\2\u01cc")
        buf.write("\u01cd\3\2\2\2\u01cd;\3\2\2\2\u01ce\u01d8\7a\2\2\u01cf")
        buf.write("\u01d0\7a\2\2\u01d0\u01d1\7\65\2\2\u01d1\u01d8\7a\2\2")
        buf.write("\u01d2\u01d3\7a\2\2\u01d3\u01d4\7\65\2\2\u01d4\u01d5\7")
        buf.write("a\2\2\u01d5\u01d6\7U\2\2\u01d6\u01d8\7a\2\2\u01d7\u01ce")
        buf.write("\3\2\2\2\u01d7\u01cf\3\2\2\2\u01d7\u01d2\3\2\2\2\u01d8")
        buf.write("=\3\2\2\2\u01d9\u01da\7\34\2\2\u01da\u01dd\5N(\2\u01db")
        buf.write("\u01dc\7V\2\2\u01dc\u01de\5\36\20\2\u01dd\u01db\3\2\2")
        buf.write("\2\u01dd\u01de\3\2\2\2\u01de\u01df\3\2\2\2\u01df\u01e1")
        buf.write("\7\b\2\2\u01e0\u01e2\7T\2\2\u01e1\u01e0\3\2\2\2\u01e1")
        buf.write("\u01e2\3\2\2\2\u01e2?\3\2\2\2\u01e3\u01e5\7\"\2\2\u01e4")
        buf.write("\u01e6\5N(\2\u01e5\u01e4\3\2\2\2\u01e5\u01e6\3\2\2\2\u01e6")
        buf.write("\u01e8\3\2\2\2\u01e7\u01e9\7T\2\2\u01e8\u01e7\3\2\2\2")
        buf.write("\u01e8\u01e9\3\2\2\2\u01e9A\3\2\2\2\u01ea\u01ec\7\35\2")
        buf.write("\2\u01eb\u01ed\7T\2\2\u01ec\u01eb\3\2\2\2\u01ec\u01ed")
        buf.write("\3\2\2\2\u01edC\3\2\2\2\u01ee\u01f0\7\36\2\2\u01ef\u01f1")
        buf.write("\7T\2\2\u01f0\u01ef\3\2\2\2\u01f0\u01f1\3\2\2\2\u01f1")
        buf.write("E\3\2\2\2\u01f2\u01f3\7\37\2\2\u01f3\u01f4\7V\2\2\u01f4")
        buf.write("\u01f5\5\36\20\2\u01f5\u01f6\7 \2\2\u01f6\u01f7\7a\2\2")
        buf.write("\u01f7\u01f8\7V\2\2\u01f8\u01f9\5\36\20\2\u01f9\u01fb")
        buf.write("\7\b\2\2\u01fa\u01fc\7T\2\2\u01fb\u01fa\3\2\2\2\u01fb")
        buf.write("\u01fc\3\2\2\2\u01fcG\3\2\2\2\u01fd\u01fe\7!\2\2\u01fe")
        buf.write("\u0200\5N(\2\u01ff\u0201\7T\2\2\u0200\u01ff\3\2\2\2\u0200")
        buf.write("\u0201\3\2\2\2\u0201I\3\2\2\2\u0202\u0203\t\2\2\2\u0203")
        buf.write("\u0205\5N(\2\u0204\u0206\7T\2\2\u0205\u0204\3\2\2\2\u0205")
        buf.write("\u0206\3\2\2\2\u0206K\3\2\2\2\u0207\u0209\5N(\2\u0208")
        buf.write("\u020a\7T\2\2\u0209\u0208\3\2\2\2\u0209\u020a\3\2\2\2")
        buf.write("\u020aM\3\2\2\2\u020b\u020c\5P)\2\u020cO\3\2\2\2\u020d")
        buf.write("\u0212\5R*\2\u020e\u020f\t\3\2\2\u020f\u0211\5R*\2\u0210")
        buf.write("\u020e\3\2\2\2\u0211\u0214\3\2\2\2\u0212\u0210\3\2\2\2")
        buf.write("\u0212\u0213\3\2\2\2\u0213Q\3\2\2\2\u0214\u0212\3\2\2")
        buf.write("\2\u0215\u021a\5T+\2\u0216\u0217\7+\2\2\u0217\u0219\5")
        buf.write("T+\2\u0218\u0216\3\2\2\2\u0219\u021c\3\2\2\2\u021a\u0218")
        buf.write("\3\2\2\2\u021a\u021b\3\2\2\2\u021bS\3\2\2\2\u021c\u021a")
        buf.write("\3\2\2\2\u021d\u0222\5V,\2\u021e\u021f\7,\2\2\u021f\u0221")
        buf.write("\5V,\2\u0220\u021e\3\2\2\2\u0221\u0224\3\2\2\2\u0222\u0220")
        buf.write("\3\2\2\2\u0222\u0223\3\2\2\2\u0223U\3\2\2\2\u0224\u0222")
        buf.write("\3\2\2\2\u0225\u022b\5Z.\2\u0226\u0227\5X-\2\u0227\u0228")
        buf.write("\5Z.\2\u0228\u022a\3\2\2\2\u0229\u0226\3\2\2\2\u022a\u022d")
        buf.write("\3\2\2\2\u022b\u0229\3\2\2\2\u022b\u022c\3\2\2\2\u022c")
        buf.write("W\3\2\2\2\u022d\u022b\3\2\2\2\u022e\u022f\t\4\2\2\u022f")
        buf.write("Y\3\2\2\2\u0230\u0236\5^\60\2\u0231\u0232\5\\/\2\u0232")
        buf.write("\u0233\5^\60\2\u0233\u0235\3\2\2\2\u0234\u0231\3\2\2\2")
        buf.write("\u0235\u0238\3\2\2\2\u0236\u0234\3\2\2\2\u0236\u0237\3")
        buf.write("\2\2\2\u0237[\3\2\2\2\u0238\u0236\3\2\2\2\u0239\u023a")
        buf.write("\t\5\2\2\u023a]\3\2\2\2\u023b\u0241\5b\62\2\u023c\u023d")
        buf.write("\5`\61\2\u023d\u023e\5b\62\2\u023e\u0240\3\2\2\2\u023f")
        buf.write("\u023c\3\2\2\2\u0240\u0243\3\2\2\2\u0241\u023f\3\2\2\2")
        buf.write("\u0241\u0242\3\2\2\2\u0242_\3\2\2\2\u0243\u0241\3\2\2")
        buf.write("\2\u0244\u0245\t\6\2\2\u0245a\3\2\2\2\u0246\u0247\t\7")
        buf.write("\2\2\u0247\u024c\5b\62\2\u0248\u0249\t\b\2\2\u0249\u024c")
        buf.write("\5b\62\2\u024a\u024c\5d\63\2\u024b\u0246\3\2\2\2\u024b")
        buf.write("\u0248\3\2\2\2\u024b\u024a\3\2\2\2\u024cc\3\2\2\2\u024d")
        buf.write("\u0263\5f\64\2\u024e\u024f\7]\2\2\u024f\u0250\7a\2\2\u0250")
        buf.write("\u0251\7^\2\2\u0251\u0253\7Y\2\2\u0252\u0254\5r:\2\u0253")
        buf.write("\u0252\3\2\2\2\u0253\u0254\3\2\2\2\u0254\u0255\3\2\2\2")
        buf.write("\u0255\u0262\7Z\2\2\u0256\u0258\7Y\2\2\u0257\u0259\5r")
        buf.write(":\2\u0258\u0257\3\2\2\2\u0258\u0259\3\2\2\2\u0259\u025a")
        buf.write("\3\2\2\2\u025a\u0262\7Z\2\2\u025b\u025c\7\65\2\2\u025c")
        buf.write("\u0262\7a\2\2\u025d\u025e\7[\2\2\u025e\u025f\5N(\2\u025f")
        buf.write("\u0260\7\\\2\2\u0260\u0262\3\2\2\2\u0261\u024e\3\2\2\2")
        buf.write("\u0261\u0256\3\2\2\2\u0261\u025b\3\2\2\2\u0261\u025d\3")
        buf.write("\2\2\2\u0262\u0265\3\2\2\2\u0263\u0261\3\2\2\2\u0263\u0264")
        buf.write("\3\2\2\2\u0264e\3\2\2\2\u0265\u0263\3\2\2\2\u0266\u0284")
        buf.write("\7_\2\2\u0267\u0284\7`\2\2\u0268\u0284\7\67\2\2\u0269")
        buf.write("\u0284\78\2\2\u026a\u0284\79\2\2\u026b\u0284\7a\2\2\u026c")
        buf.write("\u026d\7Y\2\2\u026d\u026e\5N(\2\u026e\u026f\7Z\2\2\u026f")
        buf.write("\u0284\3\2\2\2\u0270\u0271\7[\2\2\u0271\u0272\5h\65\2")
        buf.write("\u0272\u0273\7\\\2\2\u0273\u0284\3\2\2\2\u0274\u0276\7")
        buf.write("[\2\2\u0275\u0277\5r:\2\u0276\u0275\3\2\2\2\u0276\u0277")
        buf.write("\3\2\2\2\u0277\u0278\3\2\2\2\u0278\u0284\7\\\2\2\u0279")
        buf.write("\u027a\7]\2\2\u027a\u027b\7a\2\2\u027b\u0284\7^\2\2\u027c")
        buf.write("\u027d\7\23\2\2\u027d\u027e\7a\2\2\u027e\u0280\7Y\2\2")
        buf.write("\u027f\u0281\5r:\2\u0280\u027f\3\2\2\2\u0280\u0281\3\2")
        buf.write("\2\2\u0281\u0282\3\2\2\2\u0282\u0284\7Z\2\2\u0283\u0266")
        buf.write("\3\2\2\2\u0283\u0267\3\2\2\2\u0283\u0268\3\2\2\2\u0283")
        buf.write("\u0269\3\2\2\2\u0283\u026a\3\2\2\2\u0283\u026b\3\2\2\2")
        buf.write("\u0283\u026c\3\2\2\2\u0283\u0270\3\2\2\2\u0283\u0274\3")
        buf.write("\2\2\2\u0283\u0279\3\2\2\2\u0283\u027c\3\2\2\2\u0284g")
        buf.write("\3\2\2\2\u0285\u028a\5j\66\2\u0286\u0287\7U\2\2\u0287")
        buf.write("\u0289\5j\66\2\u0288\u0286\3\2\2\2\u0289\u028c\3\2\2\2")
        buf.write("\u028a\u0288\3\2\2\2\u028a\u028b\3\2\2\2\u028bi\3\2\2")
        buf.write("\2\u028c\u028a\3\2\2\2\u028d\u028e\5N(\2\u028e\u028f\7")
        buf.write("V\2\2\u028f\u0290\5N(\2\u0290k\3\2\2\2\u0291\u0295\5p")
        buf.write("9\2\u0292\u0295\5n8\2\u0293\u0295\7a\2\2\u0294\u0291\3")
        buf.write("\2\2\2\u0294\u0292\3\2\2\2\u0294\u0293\3\2\2\2\u0295m")
        buf.write("\3\2\2\2\u0296\u0297\7a\2\2\u0297\u0298\7[\2\2\u0298\u029d")
        buf.write("\5l\67\2\u0299\u029a\7U\2\2\u029a\u029c\5l\67\2\u029b")
        buf.write("\u0299\3\2\2\2\u029c\u029f\3\2\2\2\u029d\u029b\3\2\2\2")
        buf.write("\u029d\u029e\3\2\2\2\u029e\u02a0\3\2\2\2\u029f\u029d\3")
        buf.write("\2\2\2\u02a0\u02a1\7\\\2\2\u02a1o\3\2\2\2\u02a2\u02be")
        buf.write("\7:\2\2\u02a3\u02be\7;\2\2\u02a4\u02be\7<\2\2\u02a5\u02be")
        buf.write("\7=\2\2\u02a6\u02be\7A\2\2\u02a7\u02be\79\2\2\u02a8\u02be")
        buf.write("\7B\2\2\u02a9\u02be\7>\2\2\u02aa\u02be\7?\2\2\u02ab\u02be")
        buf.write("\7@\2\2\u02ac\u02ad\7>\2\2\u02ad\u02ae\7[\2\2\u02ae\u02af")
        buf.write("\5l\67\2\u02af\u02b0\7\\\2\2\u02b0\u02be\3\2\2\2\u02b1")
        buf.write("\u02b2\7?\2\2\u02b2\u02b3\7[\2\2\u02b3\u02b4\5l\67\2\u02b4")
        buf.write("\u02b5\7U\2\2\u02b5\u02b6\5l\67\2\u02b6\u02b7\7\\\2\2")
        buf.write("\u02b7\u02be\3\2\2\2\u02b8\u02b9\7@\2\2\u02b9\u02ba\7")
        buf.write("[\2\2\u02ba\u02bb\5l\67\2\u02bb\u02bc\7\\\2\2\u02bc\u02be")
        buf.write("\3\2\2\2\u02bd\u02a2\3\2\2\2\u02bd\u02a3\3\2\2\2\u02bd")
        buf.write("\u02a4\3\2\2\2\u02bd\u02a5\3\2\2\2\u02bd\u02a6\3\2\2\2")
        buf.write("\u02bd\u02a7\3\2\2\2\u02bd\u02a8\3\2\2\2\u02bd\u02a9\3")
        buf.write("\2\2\2\u02bd\u02aa\3\2\2\2\u02bd\u02ab\3\2\2\2\u02bd\u02ac")
        buf.write("\3\2\2\2\u02bd\u02b1\3\2\2\2\u02bd\u02b8\3\2\2\2\u02be")
        buf.write("q\3\2\2\2\u02bf\u02c4\5N(\2\u02c0\u02c1\7U\2\2\u02c1\u02c3")
        buf.write("\5N(\2\u02c2\u02c0\3\2\2\2\u02c3\u02c6\3\2\2\2\u02c4\u02c2")
        buf.write("\3\2\2\2\u02c4\u02c5\3\2\2\2\u02c5s\3\2\2\2\u02c6\u02c4")
        buf.write("\3\2\2\2Vy{\u0089\u0095\u0098\u00a0\u00a3\u00a9\u00ae")
        buf.write("\u00b3\u00bb\u00c0\u00c6\u00cd\u00d4\u00e0\u00e3\u00e9")
        buf.write("\u00ee\u00f2\u00f6\u00f8\u0100\u0110\u0115\u011b\u0122")
        buf.write("\u0128\u012c\u0131\u013c\u0140\u0146\u0150\u0154\u015b")
        buf.write("\u0160\u0162\u0169\u016c\u0173\u017b\u0182\u0190\u0196")
        buf.write("\u0199\u019f\u01a6\u01ad\u01b7\u01bd\u01c1\u01c8\u01cc")
        buf.write("\u01d7\u01dd\u01e1\u01e5\u01e8\u01ec\u01f0\u01fb\u0200")
        buf.write("\u0205\u0209\u0212\u021a\u0222\u022b\u0236\u0241\u024b")
        buf.write("\u0253\u0258\u0261\u0263\u0276\u0280\u0283\u028a\u0294")
        buf.write("\u029d\u02bd\u02c4")
        return buf.getvalue()


class DuanLangParser ( Parser ):

    grammarFileName = "DuanLang.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "<INVALID>", "'\u5426\u5219\u82E5'", "'\u5982\u679C'", 
                     "'\u90A3\u4E48'", "'\u5426\u5219'", "'\u7ED3\u675F'", 
                     "'\u5927\u4E8E\u7B49\u4E8E'", "'\u5C0F\u4E8E\u7B49\u4E8E'", 
                     "'\u4E0D\u7B49\u4E8E'", "'\u5927\u4E8E'", "'\u5C0F\u4E8E'", 
                     "'\u5B9A\u4E49'", "'\u7B49\u4E8E'", "'\u6BB5'", "'\u7C7B'", 
                     "'\u63A5\u53E3'", "'\u65B0'", "'\u6570\u636E\u7C7B\u578B'", 
                     "'\u9519\u8BEF'", "'\u5E38\u91CF'", "'\u7C7B\u578B'", 
                     "'\u5BFC\u51FA'", "'\u5BFC\u5165'", "'\u4ECE'", "'\u904D\u5386'", 
                     "'\u5F53'", "'\u8DF3\u51FA'", "'\u8DF3\u8FC7'", "'\u5C1D\u8BD5'", 
                     "'\u6355\u83B7'", "'\u629B\u51FA'", "'\u8FD4\u56DE'", 
                     "'\u6253\u5370'", "'\u8F93\u51FA'", "'\u8F93\u5165'", 
                     "'\u7EE7\u627F'", "'\u4F7F\u7528'", "'\u7236'", "'\u81EA\u6211'", 
                     "'\u65B9\u6CD5'", "'\u4E14'", "'\u6216'", "'\u975E'", 
                     "'\u52A0'", "'\u51CF'", "'\u4E58'", "'\u9664'", "'\u6A21'", 
                     "'\u5E42'", "'\u5E76'", "'\u4E4B'", "'\u7684'", "'\u771F'", 
                     "'\u5047'", "'\u7A7A'", "'\u6570'", "'\u6574\u6570'", 
                     "'\u6D6E\u6570'", "'\u4E32'", "'\u5217'", "'\u5178'", 
                     "'\u96C6'", "'\u5E03\u5C14'", "'\u4EFB\u610F'", "'^'", 
                     "'%'", "'*'", "'/'", "'+'", "'-'", "'=='", "'!='", 
                     "'>='", "'<='", "'>'", "'<'", "'!'", "'&&'", "'||'", 
                     "'->'", "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "<INVALID>", "'\u3001'", "<INVALID>", "<INVALID>", 
                     "<INVALID>", "<INVALID>", "'\u300A'", "'\u300B'" ]

    symbolicNames = [ "<INVALID>", "COMMENT_START", "K_ELSE_IF", "K_IF", 
                      "K_THEN", "K_ELSE", "K_END", "K_GE", "K_LE", "K_NE", 
                      "K_GT", "K_LT", "K_DEFINE", "K_EQUAL", "K_SEGMENT", 
                      "K_CLASS", "K_INTERFACE", "K_NEW", "K_DATA_TYPE", 
                      "K_ERROR_TYPE", "K_CONST", "K_TYPE", "K_EXPORT", "K_IMPORT", 
                      "K_FROM", "K_FOREACH", "K_WHILE", "K_BREAK", "K_CONTINUE", 
                      "K_TRY", "K_CATCH", "K_THROW", "K_RETURN", "K_PRINT", 
                      "K_OUTPUT", "K_INPUT", "K_INHERIT", "K_USE", "K_PARENT", 
                      "K_SELF", "K_METHOD", "K_AND", "K_OR", "K_NOT", "K_PLUS", 
                      "K_MINUS", "K_MULTIPLY", "K_DIVIDE", "K_MOD", "K_POW", 
                      "K_AND_WORD", "K_OF", "K_DE", "K_TRUE", "K_FALSE", 
                      "K_NULL", "T_NUMBER", "T_INT", "T_FLOAT", "T_STRING", 
                      "T_LIST", "T_DICT", "T_SET", "T_BOOL", "T_ANY", "POW", 
                      "MODULO", "MULTIPLY", "DIVIDE", "PLUS", "MINUS", "EQ", 
                      "NE", "GE", "LE", "GT", "LT", "NOT", "AND", "OR", 
                      "PIPE", "PATH_SEP", "DOT", "COMMA", "COLON", "SEMICOLON", 
                      "PAUSE", "LPAREN", "RPAREN", "LBRACKET", "RBRACKET", 
                      "BOOK_L", "BOOK_R", "NUMBER", "STRING", "ID", "NEWLINE", 
                      "WS", "UNKNOWN" ]

    RULE_program = 0
    RULE_moduleDecl = 1
    RULE_definition = 2
    RULE_classDef = 3
    RULE_classMember = 4
    RULE_methodDef = 5
    RULE_constructorDef = 6
    RULE_interfaceDef = 7
    RULE_interfaceMember = 8
    RULE_methodSignature = 9
    RULE_propertySignature = 10
    RULE_paragraphDef = 11
    RULE_paramList = 12
    RULE_param = 13
    RULE_block = 14
    RULE_dataTypeDef = 15
    RULE_dataTypeField = 16
    RULE_errorTypeDef = 17
    RULE_importStmt = 18
    RULE_exportStmt = 19
    RULE_path = 20
    RULE_importList = 21
    RULE_importItem = 22
    RULE_stmt = 23
    RULE_varDecl = 24
    RULE_assignStmt = 25
    RULE_target = 26
    RULE_ifStmt = 27
    RULE_foreachStmt = 28
    RULE_foreachVar = 29
    RULE_whileStmt = 30
    RULE_returnStmt = 31
    RULE_breakStmt = 32
    RULE_continueStmt = 33
    RULE_tryStmt = 34
    RULE_throwStmt = 35
    RULE_printStmt = 36
    RULE_exprStmt = 37
    RULE_expr = 38
    RULE_pipelineExpr = 39
    RULE_andExpr = 40
    RULE_orExpr = 41
    RULE_comparisonExpr = 42
    RULE_compOp = 43
    RULE_additiveExpr = 44
    RULE_addOp = 45
    RULE_multiplicativeExpr = 46
    RULE_multOp = 47
    RULE_unaryExpr = 48
    RULE_postfixExpr = 49
    RULE_primary = 50
    RULE_dictLiteral = 51
    RULE_dictEntry = 52
    RULE_typeAnnotation = 53
    RULE_genericType = 54
    RULE_builtinType = 55
    RULE_exprList = 56

    ruleNames =  [ "program", "moduleDecl", "definition", "classDef", "classMember", 
                   "methodDef", "constructorDef", "interfaceDef", "interfaceMember", 
                   "methodSignature", "propertySignature", "paragraphDef", 
                   "paramList", "param", "block", "dataTypeDef", "dataTypeField", 
                   "errorTypeDef", "importStmt", "exportStmt", "path", "importList", 
                   "importItem", "stmt", "varDecl", "assignStmt", "target", 
                   "ifStmt", "foreachStmt", "foreachVar", "whileStmt", "returnStmt", 
                   "breakStmt", "continueStmt", "tryStmt", "throwStmt", 
                   "printStmt", "exprStmt", "expr", "pipelineExpr", "andExpr", 
                   "orExpr", "comparisonExpr", "compOp", "additiveExpr", 
                   "addOp", "multiplicativeExpr", "multOp", "unaryExpr", 
                   "postfixExpr", "primary", "dictLiteral", "dictEntry", 
                   "typeAnnotation", "genericType", "builtinType", "exprList" ]

    EOF = Token.EOF
    COMMENT_START=1
    K_ELSE_IF=2
    K_IF=3
    K_THEN=4
    K_ELSE=5
    K_END=6
    K_GE=7
    K_LE=8
    K_NE=9
    K_GT=10
    K_LT=11
    K_DEFINE=12
    K_EQUAL=13
    K_SEGMENT=14
    K_CLASS=15
    K_INTERFACE=16
    K_NEW=17
    K_DATA_TYPE=18
    K_ERROR_TYPE=19
    K_CONST=20
    K_TYPE=21
    K_EXPORT=22
    K_IMPORT=23
    K_FROM=24
    K_FOREACH=25
    K_WHILE=26
    K_BREAK=27
    K_CONTINUE=28
    K_TRY=29
    K_CATCH=30
    K_THROW=31
    K_RETURN=32
    K_PRINT=33
    K_OUTPUT=34
    K_INPUT=35
    K_INHERIT=36
    K_USE=37
    K_PARENT=38
    K_SELF=39
    K_METHOD=40
    K_AND=41
    K_OR=42
    K_NOT=43
    K_PLUS=44
    K_MINUS=45
    K_MULTIPLY=46
    K_DIVIDE=47
    K_MOD=48
    K_POW=49
    K_AND_WORD=50
    K_OF=51
    K_DE=52
    K_TRUE=53
    K_FALSE=54
    K_NULL=55
    T_NUMBER=56
    T_INT=57
    T_FLOAT=58
    T_STRING=59
    T_LIST=60
    T_DICT=61
    T_SET=62
    T_BOOL=63
    T_ANY=64
    POW=65
    MODULO=66
    MULTIPLY=67
    DIVIDE=68
    PLUS=69
    MINUS=70
    EQ=71
    NE=72
    GE=73
    LE=74
    GT=75
    LT=76
    NOT=77
    AND=78
    OR=79
    PIPE=80
    PATH_SEP=81
    DOT=82
    COMMA=83
    COLON=84
    SEMICOLON=85
    PAUSE=86
    LPAREN=87
    RPAREN=88
    LBRACKET=89
    RBRACKET=90
    BOOK_L=91
    BOOK_R=92
    NUMBER=93
    STRING=94
    ID=95
    NEWLINE=96
    WS=97
    UNKNOWN=98

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.9.2")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None



    def format_error_msg(self, msg: str) -> str:
        return f"[段言语法错误] 行{self._ctx.start.line}: {msg}"



    class ProgramContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def EOF(self):
            return self.getToken(DuanLangParser.EOF, 0)

        def moduleDecl(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(DuanLangParser.ModuleDeclContext)
            else:
                return self.getTypedRuleContext(DuanLangParser.ModuleDeclContext,i)


        def importStmt(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(DuanLangParser.ImportStmtContext)
            else:
                return self.getTypedRuleContext(DuanLangParser.ImportStmtContext,i)


        def exportStmt(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(DuanLangParser.ExportStmtContext)
            else:
                return self.getTypedRuleContext(DuanLangParser.ExportStmtContext,i)


        def definition(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(DuanLangParser.DefinitionContext)
            else:
                return self.getTypedRuleContext(DuanLangParser.DefinitionContext,i)


        def stmt(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(DuanLangParser.StmtContext)
            else:
                return self.getTypedRuleContext(DuanLangParser.StmtContext,i)


        def getRuleIndex(self):
            return DuanLangParser.RULE_program

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitProgram" ):
                return visitor.visitProgram(self)
            else:
                return visitor.visitChildren(self)




    def program(self):

        localctx = DuanLangParser.ProgramContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_program)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 121
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << DuanLangParser.K_IF) | (1 << DuanLangParser.K_DEFINE) | (1 << DuanLangParser.K_NEW) | (1 << DuanLangParser.K_EXPORT) | (1 << DuanLangParser.K_IMPORT) | (1 << DuanLangParser.K_FROM) | (1 << DuanLangParser.K_FOREACH) | (1 << DuanLangParser.K_WHILE) | (1 << DuanLangParser.K_BREAK) | (1 << DuanLangParser.K_CONTINUE) | (1 << DuanLangParser.K_TRY) | (1 << DuanLangParser.K_THROW) | (1 << DuanLangParser.K_RETURN) | (1 << DuanLangParser.K_PRINT) | (1 << DuanLangParser.K_OUTPUT) | (1 << DuanLangParser.K_NOT) | (1 << DuanLangParser.K_MINUS) | (1 << DuanLangParser.K_TRUE) | (1 << DuanLangParser.K_FALSE) | (1 << DuanLangParser.K_NULL))) != 0) or ((((_la - 70)) & ~0x3f) == 0 and ((1 << (_la - 70)) & ((1 << (DuanLangParser.MINUS - 70)) | (1 << (DuanLangParser.NOT - 70)) | (1 << (DuanLangParser.LPAREN - 70)) | (1 << (DuanLangParser.LBRACKET - 70)) | (1 << (DuanLangParser.BOOK_L - 70)) | (1 << (DuanLangParser.NUMBER - 70)) | (1 << (DuanLangParser.STRING - 70)) | (1 << (DuanLangParser.ID - 70)))) != 0):
                self.state = 119
                self._errHandler.sync(self)
                la_ = self._interp.adaptivePredict(self._input,0,self._ctx)
                if la_ == 1:
                    self.state = 114
                    self.moduleDecl()
                    pass

                elif la_ == 2:
                    self.state = 115
                    self.importStmt()
                    pass

                elif la_ == 3:
                    self.state = 116
                    self.exportStmt()
                    pass

                elif la_ == 4:
                    self.state = 117
                    self.definition()
                    pass

                elif la_ == 5:
                    self.state = 118
                    self.stmt()
                    pass


                self.state = 123
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 124
            self.match(DuanLangParser.EOF)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ModuleDeclContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def LBRACKET(self):
            return self.getToken(DuanLangParser.LBRACKET, 0)

        def ID(self):
            return self.getToken(DuanLangParser.ID, 0)

        def RBRACKET(self):
            return self.getToken(DuanLangParser.RBRACKET, 0)

        def getRuleIndex(self):
            return DuanLangParser.RULE_moduleDecl

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitModuleDecl" ):
                return visitor.visitModuleDecl(self)
            else:
                return visitor.visitChildren(self)




    def moduleDecl(self):

        localctx = DuanLangParser.ModuleDeclContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_moduleDecl)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 126
            self.match(DuanLangParser.LBRACKET)
            self.state = 127
            self.match(DuanLangParser.ID)
            self.state = 128
            self.match(DuanLangParser.RBRACKET)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class DefinitionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def paragraphDef(self):
            return self.getTypedRuleContext(DuanLangParser.ParagraphDefContext,0)


        def classDef(self):
            return self.getTypedRuleContext(DuanLangParser.ClassDefContext,0)


        def interfaceDef(self):
            return self.getTypedRuleContext(DuanLangParser.InterfaceDefContext,0)


        def dataTypeDef(self):
            return self.getTypedRuleContext(DuanLangParser.DataTypeDefContext,0)


        def errorTypeDef(self):
            return self.getTypedRuleContext(DuanLangParser.ErrorTypeDefContext,0)


        def getRuleIndex(self):
            return DuanLangParser.RULE_definition

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitDefinition" ):
                return visitor.visitDefinition(self)
            else:
                return visitor.visitChildren(self)




    def definition(self):

        localctx = DuanLangParser.DefinitionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_definition)
        try:
            self.state = 135
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,2,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 130
                self.paragraphDef()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 131
                self.classDef()
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 132
                self.interfaceDef()
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 133
                self.dataTypeDef()
                pass

            elif la_ == 5:
                self.enterOuterAlt(localctx, 5)
                self.state = 134
                self.errorTypeDef()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ClassDefContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def BOOK_L(self):
            return self.getToken(DuanLangParser.BOOK_L, 0)

        def ID(self):
            return self.getToken(DuanLangParser.ID, 0)

        def BOOK_R(self):
            return self.getToken(DuanLangParser.BOOK_R, 0)

        def K_CLASS(self):
            return self.getToken(DuanLangParser.K_CLASS, 0)

        def COLON(self):
            return self.getToken(DuanLangParser.COLON, 0)

        def K_END(self):
            return self.getToken(DuanLangParser.K_END, 0)

        def K_INHERIT(self):
            return self.getToken(DuanLangParser.K_INHERIT, 0)

        def typeAnnotation(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(DuanLangParser.TypeAnnotationContext)
            else:
                return self.getTypedRuleContext(DuanLangParser.TypeAnnotationContext,i)


        def K_USE(self):
            return self.getToken(DuanLangParser.K_USE, 0)

        def classMember(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(DuanLangParser.ClassMemberContext)
            else:
                return self.getTypedRuleContext(DuanLangParser.ClassMemberContext,i)


        def DOT(self):
            return self.getToken(DuanLangParser.DOT, 0)

        def COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(DuanLangParser.COMMA)
            else:
                return self.getToken(DuanLangParser.COMMA, i)

        def getRuleIndex(self):
            return DuanLangParser.RULE_classDef

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitClassDef" ):
                return visitor.visitClassDef(self)
            else:
                return visitor.visitChildren(self)




    def classDef(self):

        localctx = DuanLangParser.ClassDefContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_classDef)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 137
            self.match(DuanLangParser.BOOK_L)
            self.state = 138
            self.match(DuanLangParser.ID)
            self.state = 139
            self.match(DuanLangParser.BOOK_R)
            self.state = 140
            self.match(DuanLangParser.K_CLASS)
            self.state = 150
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==DuanLangParser.K_INHERIT:
                self.state = 141
                self.match(DuanLangParser.K_INHERIT)
                self.state = 142
                self.typeAnnotation()
                self.state = 147
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la==DuanLangParser.COMMA:
                    self.state = 143
                    self.match(DuanLangParser.COMMA)
                    self.state = 144
                    self.typeAnnotation()
                    self.state = 149
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)



            self.state = 161
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==DuanLangParser.K_USE:
                self.state = 152
                self.match(DuanLangParser.K_USE)
                self.state = 153
                self.typeAnnotation()
                self.state = 158
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la==DuanLangParser.COMMA:
                    self.state = 154
                    self.match(DuanLangParser.COMMA)
                    self.state = 155
                    self.typeAnnotation()
                    self.state = 160
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)



            self.state = 163
            self.match(DuanLangParser.COLON)
            self.state = 167
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==DuanLangParser.K_DEFINE or _la==DuanLangParser.BOOK_L:
                self.state = 164
                self.classMember()
                self.state = 169
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 170
            self.match(DuanLangParser.K_END)
            self.state = 172
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==DuanLangParser.DOT:
                self.state = 171
                self.match(DuanLangParser.DOT)


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ClassMemberContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def varDecl(self):
            return self.getTypedRuleContext(DuanLangParser.VarDeclContext,0)


        def methodDef(self):
            return self.getTypedRuleContext(DuanLangParser.MethodDefContext,0)


        def constructorDef(self):
            return self.getTypedRuleContext(DuanLangParser.ConstructorDefContext,0)


        def getRuleIndex(self):
            return DuanLangParser.RULE_classMember

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitClassMember" ):
                return visitor.visitClassMember(self)
            else:
                return visitor.visitChildren(self)




    def classMember(self):

        localctx = DuanLangParser.ClassMemberContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_classMember)
        try:
            self.state = 177
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,9,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 174
                self.varDecl()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 175
                self.methodDef()
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 176
                self.constructorDef()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class MethodDefContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def BOOK_L(self):
            return self.getToken(DuanLangParser.BOOK_L, 0)

        def ID(self):
            return self.getToken(DuanLangParser.ID, 0)

        def BOOK_R(self):
            return self.getToken(DuanLangParser.BOOK_R, 0)

        def K_METHOD(self):
            return self.getToken(DuanLangParser.K_METHOD, 0)

        def LPAREN(self):
            return self.getToken(DuanLangParser.LPAREN, 0)

        def RPAREN(self):
            return self.getToken(DuanLangParser.RPAREN, 0)

        def COLON(self):
            return self.getToken(DuanLangParser.COLON, 0)

        def block(self):
            return self.getTypedRuleContext(DuanLangParser.BlockContext,0)


        def K_END(self):
            return self.getToken(DuanLangParser.K_END, 0)

        def paramList(self):
            return self.getTypedRuleContext(DuanLangParser.ParamListContext,0)


        def PIPE(self):
            return self.getToken(DuanLangParser.PIPE, 0)

        def typeAnnotation(self):
            return self.getTypedRuleContext(DuanLangParser.TypeAnnotationContext,0)


        def DOT(self):
            return self.getToken(DuanLangParser.DOT, 0)

        def getRuleIndex(self):
            return DuanLangParser.RULE_methodDef

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitMethodDef" ):
                return visitor.visitMethodDef(self)
            else:
                return visitor.visitChildren(self)




    def methodDef(self):

        localctx = DuanLangParser.MethodDefContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_methodDef)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 179
            self.match(DuanLangParser.BOOK_L)
            self.state = 180
            self.match(DuanLangParser.ID)
            self.state = 181
            self.match(DuanLangParser.BOOK_R)
            self.state = 182
            self.match(DuanLangParser.K_METHOD)
            self.state = 183
            self.match(DuanLangParser.LPAREN)
            self.state = 185
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==DuanLangParser.ID:
                self.state = 184
                self.paramList()


            self.state = 187
            self.match(DuanLangParser.RPAREN)
            self.state = 190
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==DuanLangParser.PIPE:
                self.state = 188
                self.match(DuanLangParser.PIPE)
                self.state = 189
                self.typeAnnotation()


            self.state = 192
            self.match(DuanLangParser.COLON)
            self.state = 193
            self.block()
            self.state = 194
            self.match(DuanLangParser.K_END)
            self.state = 196
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==DuanLangParser.DOT:
                self.state = 195
                self.match(DuanLangParser.DOT)


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ConstructorDefContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def BOOK_L(self):
            return self.getToken(DuanLangParser.BOOK_L, 0)

        def ID(self):
            return self.getToken(DuanLangParser.ID, 0)

        def BOOK_R(self):
            return self.getToken(DuanLangParser.BOOK_R, 0)

        def LPAREN(self):
            return self.getToken(DuanLangParser.LPAREN, 0)

        def RPAREN(self):
            return self.getToken(DuanLangParser.RPAREN, 0)

        def COLON(self):
            return self.getToken(DuanLangParser.COLON, 0)

        def block(self):
            return self.getTypedRuleContext(DuanLangParser.BlockContext,0)


        def K_END(self):
            return self.getToken(DuanLangParser.K_END, 0)

        def paramList(self):
            return self.getTypedRuleContext(DuanLangParser.ParamListContext,0)


        def DOT(self):
            return self.getToken(DuanLangParser.DOT, 0)

        def getRuleIndex(self):
            return DuanLangParser.RULE_constructorDef

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitConstructorDef" ):
                return visitor.visitConstructorDef(self)
            else:
                return visitor.visitChildren(self)




    def constructorDef(self):

        localctx = DuanLangParser.ConstructorDefContext(self, self._ctx, self.state)
        self.enterRule(localctx, 12, self.RULE_constructorDef)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 198
            self.match(DuanLangParser.BOOK_L)
            self.state = 199
            self.match(DuanLangParser.ID)
            self.state = 200
            self.match(DuanLangParser.BOOK_R)
            self.state = 201
            self.match(DuanLangParser.LPAREN)
            self.state = 203
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==DuanLangParser.ID:
                self.state = 202
                self.paramList()


            self.state = 205
            self.match(DuanLangParser.RPAREN)
            self.state = 206
            self.match(DuanLangParser.COLON)
            self.state = 207
            self.block()
            self.state = 208
            self.match(DuanLangParser.K_END)
            self.state = 210
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==DuanLangParser.DOT:
                self.state = 209
                self.match(DuanLangParser.DOT)


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class InterfaceDefContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def BOOK_L(self):
            return self.getToken(DuanLangParser.BOOK_L, 0)

        def ID(self):
            return self.getToken(DuanLangParser.ID, 0)

        def BOOK_R(self):
            return self.getToken(DuanLangParser.BOOK_R, 0)

        def K_INTERFACE(self):
            return self.getToken(DuanLangParser.K_INTERFACE, 0)

        def COLON(self):
            return self.getToken(DuanLangParser.COLON, 0)

        def K_END(self):
            return self.getToken(DuanLangParser.K_END, 0)

        def K_INHERIT(self):
            return self.getToken(DuanLangParser.K_INHERIT, 0)

        def typeAnnotation(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(DuanLangParser.TypeAnnotationContext)
            else:
                return self.getTypedRuleContext(DuanLangParser.TypeAnnotationContext,i)


        def interfaceMember(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(DuanLangParser.InterfaceMemberContext)
            else:
                return self.getTypedRuleContext(DuanLangParser.InterfaceMemberContext,i)


        def DOT(self):
            return self.getToken(DuanLangParser.DOT, 0)

        def COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(DuanLangParser.COMMA)
            else:
                return self.getToken(DuanLangParser.COMMA, i)

        def getRuleIndex(self):
            return DuanLangParser.RULE_interfaceDef

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitInterfaceDef" ):
                return visitor.visitInterfaceDef(self)
            else:
                return visitor.visitChildren(self)




    def interfaceDef(self):

        localctx = DuanLangParser.InterfaceDefContext(self, self._ctx, self.state)
        self.enterRule(localctx, 14, self.RULE_interfaceDef)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 212
            self.match(DuanLangParser.BOOK_L)
            self.state = 213
            self.match(DuanLangParser.ID)
            self.state = 214
            self.match(DuanLangParser.BOOK_R)
            self.state = 215
            self.match(DuanLangParser.K_INTERFACE)
            self.state = 225
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==DuanLangParser.K_INHERIT:
                self.state = 216
                self.match(DuanLangParser.K_INHERIT)
                self.state = 217
                self.typeAnnotation()
                self.state = 222
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la==DuanLangParser.COMMA:
                    self.state = 218
                    self.match(DuanLangParser.COMMA)
                    self.state = 219
                    self.typeAnnotation()
                    self.state = 224
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)



            self.state = 227
            self.match(DuanLangParser.COLON)
            self.state = 231
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==DuanLangParser.BOOK_L or _la==DuanLangParser.ID:
                self.state = 228
                self.interfaceMember()
                self.state = 233
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 234
            self.match(DuanLangParser.K_END)
            self.state = 236
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==DuanLangParser.DOT:
                self.state = 235
                self.match(DuanLangParser.DOT)


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class InterfaceMemberContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def methodSignature(self):
            return self.getTypedRuleContext(DuanLangParser.MethodSignatureContext,0)


        def DOT(self):
            return self.getToken(DuanLangParser.DOT, 0)

        def propertySignature(self):
            return self.getTypedRuleContext(DuanLangParser.PropertySignatureContext,0)


        def getRuleIndex(self):
            return DuanLangParser.RULE_interfaceMember

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitInterfaceMember" ):
                return visitor.visitInterfaceMember(self)
            else:
                return visitor.visitChildren(self)




    def interfaceMember(self):

        localctx = DuanLangParser.InterfaceMemberContext(self, self._ctx, self.state)
        self.enterRule(localctx, 16, self.RULE_interfaceMember)
        self._la = 0 # Token type
        try:
            self.state = 246
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [DuanLangParser.BOOK_L]:
                self.enterOuterAlt(localctx, 1)
                self.state = 238
                self.methodSignature()
                self.state = 240
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==DuanLangParser.DOT:
                    self.state = 239
                    self.match(DuanLangParser.DOT)


                pass
            elif token in [DuanLangParser.ID]:
                self.enterOuterAlt(localctx, 2)
                self.state = 242
                self.propertySignature()
                self.state = 244
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==DuanLangParser.DOT:
                    self.state = 243
                    self.match(DuanLangParser.DOT)


                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class MethodSignatureContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def BOOK_L(self):
            return self.getToken(DuanLangParser.BOOK_L, 0)

        def ID(self):
            return self.getToken(DuanLangParser.ID, 0)

        def BOOK_R(self):
            return self.getToken(DuanLangParser.BOOK_R, 0)

        def K_METHOD(self):
            return self.getToken(DuanLangParser.K_METHOD, 0)

        def LPAREN(self):
            return self.getToken(DuanLangParser.LPAREN, 0)

        def RPAREN(self):
            return self.getToken(DuanLangParser.RPAREN, 0)

        def PIPE(self):
            return self.getToken(DuanLangParser.PIPE, 0)

        def typeAnnotation(self):
            return self.getTypedRuleContext(DuanLangParser.TypeAnnotationContext,0)


        def paramList(self):
            return self.getTypedRuleContext(DuanLangParser.ParamListContext,0)


        def getRuleIndex(self):
            return DuanLangParser.RULE_methodSignature

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitMethodSignature" ):
                return visitor.visitMethodSignature(self)
            else:
                return visitor.visitChildren(self)




    def methodSignature(self):

        localctx = DuanLangParser.MethodSignatureContext(self, self._ctx, self.state)
        self.enterRule(localctx, 18, self.RULE_methodSignature)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 248
            self.match(DuanLangParser.BOOK_L)
            self.state = 249
            self.match(DuanLangParser.ID)
            self.state = 250
            self.match(DuanLangParser.BOOK_R)
            self.state = 251
            self.match(DuanLangParser.K_METHOD)
            self.state = 252
            self.match(DuanLangParser.LPAREN)
            self.state = 254
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==DuanLangParser.ID:
                self.state = 253
                self.paramList()


            self.state = 256
            self.match(DuanLangParser.RPAREN)
            self.state = 257
            self.match(DuanLangParser.PIPE)
            self.state = 258
            self.typeAnnotation()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class PropertySignatureContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ID(self):
            return self.getToken(DuanLangParser.ID, 0)

        def COLON(self):
            return self.getToken(DuanLangParser.COLON, 0)

        def typeAnnotation(self):
            return self.getTypedRuleContext(DuanLangParser.TypeAnnotationContext,0)


        def getRuleIndex(self):
            return DuanLangParser.RULE_propertySignature

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitPropertySignature" ):
                return visitor.visitPropertySignature(self)
            else:
                return visitor.visitChildren(self)




    def propertySignature(self):

        localctx = DuanLangParser.PropertySignatureContext(self, self._ctx, self.state)
        self.enterRule(localctx, 20, self.RULE_propertySignature)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 260
            self.match(DuanLangParser.ID)
            self.state = 261
            self.match(DuanLangParser.COLON)
            self.state = 262
            self.typeAnnotation()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ParagraphDefContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def BOOK_L(self):
            return self.getToken(DuanLangParser.BOOK_L, 0)

        def ID(self):
            return self.getToken(DuanLangParser.ID, 0)

        def BOOK_R(self):
            return self.getToken(DuanLangParser.BOOK_R, 0)

        def K_SEGMENT(self):
            return self.getToken(DuanLangParser.K_SEGMENT, 0)

        def LPAREN(self):
            return self.getToken(DuanLangParser.LPAREN, 0)

        def RPAREN(self):
            return self.getToken(DuanLangParser.RPAREN, 0)

        def COLON(self):
            return self.getToken(DuanLangParser.COLON, 0)

        def block(self):
            return self.getTypedRuleContext(DuanLangParser.BlockContext,0)


        def K_END(self):
            return self.getToken(DuanLangParser.K_END, 0)

        def paramList(self):
            return self.getTypedRuleContext(DuanLangParser.ParamListContext,0)


        def PIPE(self):
            return self.getToken(DuanLangParser.PIPE, 0)

        def typeAnnotation(self):
            return self.getTypedRuleContext(DuanLangParser.TypeAnnotationContext,0)


        def DOT(self):
            return self.getToken(DuanLangParser.DOT, 0)

        def getRuleIndex(self):
            return DuanLangParser.RULE_paragraphDef

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitParagraphDef" ):
                return visitor.visitParagraphDef(self)
            else:
                return visitor.visitChildren(self)




    def paragraphDef(self):

        localctx = DuanLangParser.ParagraphDefContext(self, self._ctx, self.state)
        self.enterRule(localctx, 22, self.RULE_paragraphDef)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 264
            self.match(DuanLangParser.BOOK_L)
            self.state = 265
            self.match(DuanLangParser.ID)
            self.state = 266
            self.match(DuanLangParser.BOOK_R)
            self.state = 267
            self.match(DuanLangParser.K_SEGMENT)
            self.state = 268
            self.match(DuanLangParser.LPAREN)
            self.state = 270
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==DuanLangParser.ID:
                self.state = 269
                self.paramList()


            self.state = 272
            self.match(DuanLangParser.RPAREN)
            self.state = 275
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==DuanLangParser.PIPE:
                self.state = 273
                self.match(DuanLangParser.PIPE)
                self.state = 274
                self.typeAnnotation()


            self.state = 277
            self.match(DuanLangParser.COLON)
            self.state = 278
            self.block()
            self.state = 279
            self.match(DuanLangParser.K_END)
            self.state = 281
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==DuanLangParser.DOT:
                self.state = 280
                self.match(DuanLangParser.DOT)


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ParamListContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def param(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(DuanLangParser.ParamContext)
            else:
                return self.getTypedRuleContext(DuanLangParser.ParamContext,i)


        def COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(DuanLangParser.COMMA)
            else:
                return self.getToken(DuanLangParser.COMMA, i)

        def getRuleIndex(self):
            return DuanLangParser.RULE_paramList

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitParamList" ):
                return visitor.visitParamList(self)
            else:
                return visitor.visitChildren(self)




    def paramList(self):

        localctx = DuanLangParser.ParamListContext(self, self._ctx, self.state)
        self.enterRule(localctx, 24, self.RULE_paramList)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 283
            self.param()
            self.state = 288
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==DuanLangParser.COMMA:
                self.state = 284
                self.match(DuanLangParser.COMMA)
                self.state = 285
                self.param()
                self.state = 290
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ParamContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ID(self):
            return self.getToken(DuanLangParser.ID, 0)

        def COLON(self):
            return self.getToken(DuanLangParser.COLON, 0)

        def typeAnnotation(self):
            return self.getTypedRuleContext(DuanLangParser.TypeAnnotationContext,0)


        def K_EQUAL(self):
            return self.getToken(DuanLangParser.K_EQUAL, 0)

        def expr(self):
            return self.getTypedRuleContext(DuanLangParser.ExprContext,0)


        def getRuleIndex(self):
            return DuanLangParser.RULE_param

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitParam" ):
                return visitor.visitParam(self)
            else:
                return visitor.visitChildren(self)




    def param(self):

        localctx = DuanLangParser.ParamContext(self, self._ctx, self.state)
        self.enterRule(localctx, 26, self.RULE_param)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 291
            self.match(DuanLangParser.ID)
            self.state = 294
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==DuanLangParser.COLON:
                self.state = 292
                self.match(DuanLangParser.COLON)
                self.state = 293
                self.typeAnnotation()


            self.state = 298
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==DuanLangParser.K_EQUAL:
                self.state = 296
                self.match(DuanLangParser.K_EQUAL)
                self.state = 297
                self.expr()


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class BlockContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def stmt(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(DuanLangParser.StmtContext)
            else:
                return self.getTypedRuleContext(DuanLangParser.StmtContext,i)


        def getRuleIndex(self):
            return DuanLangParser.RULE_block

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitBlock" ):
                return visitor.visitBlock(self)
            else:
                return visitor.visitChildren(self)




    def block(self):

        localctx = DuanLangParser.BlockContext(self, self._ctx, self.state)
        self.enterRule(localctx, 28, self.RULE_block)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 303
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << DuanLangParser.K_IF) | (1 << DuanLangParser.K_DEFINE) | (1 << DuanLangParser.K_NEW) | (1 << DuanLangParser.K_FOREACH) | (1 << DuanLangParser.K_WHILE) | (1 << DuanLangParser.K_BREAK) | (1 << DuanLangParser.K_CONTINUE) | (1 << DuanLangParser.K_TRY) | (1 << DuanLangParser.K_THROW) | (1 << DuanLangParser.K_RETURN) | (1 << DuanLangParser.K_PRINT) | (1 << DuanLangParser.K_OUTPUT) | (1 << DuanLangParser.K_NOT) | (1 << DuanLangParser.K_MINUS) | (1 << DuanLangParser.K_TRUE) | (1 << DuanLangParser.K_FALSE) | (1 << DuanLangParser.K_NULL))) != 0) or ((((_la - 70)) & ~0x3f) == 0 and ((1 << (_la - 70)) & ((1 << (DuanLangParser.MINUS - 70)) | (1 << (DuanLangParser.NOT - 70)) | (1 << (DuanLangParser.LPAREN - 70)) | (1 << (DuanLangParser.LBRACKET - 70)) | (1 << (DuanLangParser.BOOK_L - 70)) | (1 << (DuanLangParser.NUMBER - 70)) | (1 << (DuanLangParser.STRING - 70)) | (1 << (DuanLangParser.ID - 70)))) != 0):
                self.state = 300
                self.stmt()
                self.state = 305
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class DataTypeDefContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def BOOK_L(self):
            return self.getToken(DuanLangParser.BOOK_L, 0)

        def ID(self):
            return self.getToken(DuanLangParser.ID, 0)

        def BOOK_R(self):
            return self.getToken(DuanLangParser.BOOK_R, 0)

        def K_DATA_TYPE(self):
            return self.getToken(DuanLangParser.K_DATA_TYPE, 0)

        def COLON(self):
            return self.getToken(DuanLangParser.COLON, 0)

        def K_END(self):
            return self.getToken(DuanLangParser.K_END, 0)

        def dataTypeField(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(DuanLangParser.DataTypeFieldContext)
            else:
                return self.getTypedRuleContext(DuanLangParser.DataTypeFieldContext,i)


        def DOT(self):
            return self.getToken(DuanLangParser.DOT, 0)

        def getRuleIndex(self):
            return DuanLangParser.RULE_dataTypeDef

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitDataTypeDef" ):
                return visitor.visitDataTypeDef(self)
            else:
                return visitor.visitChildren(self)




    def dataTypeDef(self):

        localctx = DuanLangParser.DataTypeDefContext(self, self._ctx, self.state)
        self.enterRule(localctx, 30, self.RULE_dataTypeDef)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 306
            self.match(DuanLangParser.BOOK_L)
            self.state = 307
            self.match(DuanLangParser.ID)
            self.state = 308
            self.match(DuanLangParser.BOOK_R)
            self.state = 309
            self.match(DuanLangParser.K_DATA_TYPE)
            self.state = 310
            self.match(DuanLangParser.COLON)
            self.state = 312 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 311
                self.dataTypeField()
                self.state = 314 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not (_la==DuanLangParser.ID):
                    break

            self.state = 316
            self.match(DuanLangParser.K_END)
            self.state = 318
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==DuanLangParser.DOT:
                self.state = 317
                self.match(DuanLangParser.DOT)


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class DataTypeFieldContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ID(self):
            return self.getToken(DuanLangParser.ID, 0)

        def COLON(self):
            return self.getToken(DuanLangParser.COLON, 0)

        def typeAnnotation(self):
            return self.getTypedRuleContext(DuanLangParser.TypeAnnotationContext,0)


        def DOT(self):
            return self.getToken(DuanLangParser.DOT, 0)

        def getRuleIndex(self):
            return DuanLangParser.RULE_dataTypeField

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitDataTypeField" ):
                return visitor.visitDataTypeField(self)
            else:
                return visitor.visitChildren(self)




    def dataTypeField(self):

        localctx = DuanLangParser.DataTypeFieldContext(self, self._ctx, self.state)
        self.enterRule(localctx, 32, self.RULE_dataTypeField)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 320
            self.match(DuanLangParser.ID)
            self.state = 321
            self.match(DuanLangParser.COLON)
            self.state = 322
            self.typeAnnotation()
            self.state = 324
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==DuanLangParser.DOT:
                self.state = 323
                self.match(DuanLangParser.DOT)


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ErrorTypeDefContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def BOOK_L(self):
            return self.getToken(DuanLangParser.BOOK_L, 0)

        def ID(self):
            return self.getToken(DuanLangParser.ID, 0)

        def BOOK_R(self):
            return self.getToken(DuanLangParser.BOOK_R, 0)

        def K_ERROR_TYPE(self):
            return self.getToken(DuanLangParser.K_ERROR_TYPE, 0)

        def COLON(self):
            return self.getToken(DuanLangParser.COLON, 0)

        def K_END(self):
            return self.getToken(DuanLangParser.K_END, 0)

        def dataTypeField(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(DuanLangParser.DataTypeFieldContext)
            else:
                return self.getTypedRuleContext(DuanLangParser.DataTypeFieldContext,i)


        def DOT(self):
            return self.getToken(DuanLangParser.DOT, 0)

        def getRuleIndex(self):
            return DuanLangParser.RULE_errorTypeDef

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitErrorTypeDef" ):
                return visitor.visitErrorTypeDef(self)
            else:
                return visitor.visitChildren(self)




    def errorTypeDef(self):

        localctx = DuanLangParser.ErrorTypeDefContext(self, self._ctx, self.state)
        self.enterRule(localctx, 34, self.RULE_errorTypeDef)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 326
            self.match(DuanLangParser.BOOK_L)
            self.state = 327
            self.match(DuanLangParser.ID)
            self.state = 328
            self.match(DuanLangParser.BOOK_R)
            self.state = 329
            self.match(DuanLangParser.K_ERROR_TYPE)
            self.state = 330
            self.match(DuanLangParser.COLON)
            self.state = 332 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 331
                self.dataTypeField()
                self.state = 334 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not (_la==DuanLangParser.ID):
                    break

            self.state = 336
            self.match(DuanLangParser.K_END)
            self.state = 338
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==DuanLangParser.DOT:
                self.state = 337
                self.match(DuanLangParser.DOT)


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ImportStmtContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def K_FROM(self):
            return self.getToken(DuanLangParser.K_FROM, 0)

        def path(self):
            return self.getTypedRuleContext(DuanLangParser.PathContext,0)


        def K_IMPORT(self):
            return self.getToken(DuanLangParser.K_IMPORT, 0)

        def importList(self):
            return self.getTypedRuleContext(DuanLangParser.ImportListContext,0)


        def DOT(self):
            return self.getToken(DuanLangParser.DOT, 0)

        def getRuleIndex(self):
            return DuanLangParser.RULE_importStmt

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitImportStmt" ):
                return visitor.visitImportStmt(self)
            else:
                return visitor.visitChildren(self)




    def importStmt(self):

        localctx = DuanLangParser.ImportStmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 36, self.RULE_importStmt)
        self._la = 0 # Token type
        try:
            self.state = 352
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [DuanLangParser.K_FROM]:
                self.enterOuterAlt(localctx, 1)
                self.state = 340
                self.match(DuanLangParser.K_FROM)
                self.state = 341
                self.path()
                self.state = 342
                self.match(DuanLangParser.K_IMPORT)
                self.state = 343
                self.importList()
                self.state = 345
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==DuanLangParser.DOT:
                    self.state = 344
                    self.match(DuanLangParser.DOT)


                pass
            elif token in [DuanLangParser.K_IMPORT]:
                self.enterOuterAlt(localctx, 2)
                self.state = 347
                self.match(DuanLangParser.K_IMPORT)
                self.state = 348
                self.importList()
                self.state = 350
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==DuanLangParser.DOT:
                    self.state = 349
                    self.match(DuanLangParser.DOT)


                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ExportStmtContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def K_EXPORT(self):
            return self.getToken(DuanLangParser.K_EXPORT, 0)

        def ID(self):
            return self.getToken(DuanLangParser.ID, 0)

        def BOOK_L(self):
            return self.getToken(DuanLangParser.BOOK_L, 0)

        def BOOK_R(self):
            return self.getToken(DuanLangParser.BOOK_R, 0)

        def DOT(self):
            return self.getToken(DuanLangParser.DOT, 0)

        def getRuleIndex(self):
            return DuanLangParser.RULE_exportStmt

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitExportStmt" ):
                return visitor.visitExportStmt(self)
            else:
                return visitor.visitChildren(self)




    def exportStmt(self):

        localctx = DuanLangParser.ExportStmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 38, self.RULE_exportStmt)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 354
            self.match(DuanLangParser.K_EXPORT)
            self.state = 359
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [DuanLangParser.ID]:
                self.state = 355
                self.match(DuanLangParser.ID)
                pass
            elif token in [DuanLangParser.BOOK_L]:
                self.state = 356
                self.match(DuanLangParser.BOOK_L)
                self.state = 357
                self.match(DuanLangParser.ID)
                self.state = 358
                self.match(DuanLangParser.BOOK_R)
                pass
            else:
                raise NoViableAltException(self)

            self.state = 362
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==DuanLangParser.DOT:
                self.state = 361
                self.match(DuanLangParser.DOT)


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class PathContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ID(self, i:int=None):
            if i is None:
                return self.getTokens(DuanLangParser.ID)
            else:
                return self.getToken(DuanLangParser.ID, i)

        def PATH_SEP(self, i:int=None):
            if i is None:
                return self.getTokens(DuanLangParser.PATH_SEP)
            else:
                return self.getToken(DuanLangParser.PATH_SEP, i)

        def getRuleIndex(self):
            return DuanLangParser.RULE_path

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitPath" ):
                return visitor.visitPath(self)
            else:
                return visitor.visitChildren(self)




    def path(self):

        localctx = DuanLangParser.PathContext(self, self._ctx, self.state)
        self.enterRule(localctx, 40, self.RULE_path)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 364
            self.match(DuanLangParser.ID)
            self.state = 369
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==DuanLangParser.PATH_SEP:
                self.state = 365
                self.match(DuanLangParser.PATH_SEP)
                self.state = 366
                self.match(DuanLangParser.ID)
                self.state = 371
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ImportListContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def importItem(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(DuanLangParser.ImportItemContext)
            else:
                return self.getTypedRuleContext(DuanLangParser.ImportItemContext,i)


        def COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(DuanLangParser.COMMA)
            else:
                return self.getToken(DuanLangParser.COMMA, i)

        def getRuleIndex(self):
            return DuanLangParser.RULE_importList

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitImportList" ):
                return visitor.visitImportList(self)
            else:
                return visitor.visitChildren(self)




    def importList(self):

        localctx = DuanLangParser.ImportListContext(self, self._ctx, self.state)
        self.enterRule(localctx, 42, self.RULE_importList)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 372
            self.importItem()
            self.state = 377
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==DuanLangParser.COMMA:
                self.state = 373
                self.match(DuanLangParser.COMMA)
                self.state = 374
                self.importItem()
                self.state = 379
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ImportItemContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def BOOK_L(self):
            return self.getToken(DuanLangParser.BOOK_L, 0)

        def ID(self):
            return self.getToken(DuanLangParser.ID, 0)

        def BOOK_R(self):
            return self.getToken(DuanLangParser.BOOK_R, 0)

        def getRuleIndex(self):
            return DuanLangParser.RULE_importItem

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitImportItem" ):
                return visitor.visitImportItem(self)
            else:
                return visitor.visitChildren(self)




    def importItem(self):

        localctx = DuanLangParser.ImportItemContext(self, self._ctx, self.state)
        self.enterRule(localctx, 44, self.RULE_importItem)
        try:
            self.state = 384
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [DuanLangParser.BOOK_L]:
                self.enterOuterAlt(localctx, 1)
                self.state = 380
                self.match(DuanLangParser.BOOK_L)
                self.state = 381
                self.match(DuanLangParser.ID)
                self.state = 382
                self.match(DuanLangParser.BOOK_R)
                pass
            elif token in [DuanLangParser.ID]:
                self.enterOuterAlt(localctx, 2)
                self.state = 383
                self.match(DuanLangParser.ID)
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class StmtContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def varDecl(self):
            return self.getTypedRuleContext(DuanLangParser.VarDeclContext,0)


        def assignStmt(self):
            return self.getTypedRuleContext(DuanLangParser.AssignStmtContext,0)


        def ifStmt(self):
            return self.getTypedRuleContext(DuanLangParser.IfStmtContext,0)


        def foreachStmt(self):
            return self.getTypedRuleContext(DuanLangParser.ForeachStmtContext,0)


        def whileStmt(self):
            return self.getTypedRuleContext(DuanLangParser.WhileStmtContext,0)


        def returnStmt(self):
            return self.getTypedRuleContext(DuanLangParser.ReturnStmtContext,0)


        def breakStmt(self):
            return self.getTypedRuleContext(DuanLangParser.BreakStmtContext,0)


        def continueStmt(self):
            return self.getTypedRuleContext(DuanLangParser.ContinueStmtContext,0)


        def tryStmt(self):
            return self.getTypedRuleContext(DuanLangParser.TryStmtContext,0)


        def throwStmt(self):
            return self.getTypedRuleContext(DuanLangParser.ThrowStmtContext,0)


        def printStmt(self):
            return self.getTypedRuleContext(DuanLangParser.PrintStmtContext,0)


        def exprStmt(self):
            return self.getTypedRuleContext(DuanLangParser.ExprStmtContext,0)


        def getRuleIndex(self):
            return DuanLangParser.RULE_stmt

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitStmt" ):
                return visitor.visitStmt(self)
            else:
                return visitor.visitChildren(self)




    def stmt(self):

        localctx = DuanLangParser.StmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 46, self.RULE_stmt)
        try:
            self.state = 398
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,43,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 386
                self.varDecl()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 387
                self.assignStmt()
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 388
                self.ifStmt()
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 389
                self.foreachStmt()
                pass

            elif la_ == 5:
                self.enterOuterAlt(localctx, 5)
                self.state = 390
                self.whileStmt()
                pass

            elif la_ == 6:
                self.enterOuterAlt(localctx, 6)
                self.state = 391
                self.returnStmt()
                pass

            elif la_ == 7:
                self.enterOuterAlt(localctx, 7)
                self.state = 392
                self.breakStmt()
                pass

            elif la_ == 8:
                self.enterOuterAlt(localctx, 8)
                self.state = 393
                self.continueStmt()
                pass

            elif la_ == 9:
                self.enterOuterAlt(localctx, 9)
                self.state = 394
                self.tryStmt()
                pass

            elif la_ == 10:
                self.enterOuterAlt(localctx, 10)
                self.state = 395
                self.throwStmt()
                pass

            elif la_ == 11:
                self.enterOuterAlt(localctx, 11)
                self.state = 396
                self.printStmt()
                pass

            elif la_ == 12:
                self.enterOuterAlt(localctx, 12)
                self.state = 397
                self.exprStmt()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class VarDeclContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def K_DEFINE(self):
            return self.getToken(DuanLangParser.K_DEFINE, 0)

        def ID(self):
            return self.getToken(DuanLangParser.ID, 0)

        def K_EQUAL(self):
            return self.getToken(DuanLangParser.K_EQUAL, 0)

        def expr(self):
            return self.getTypedRuleContext(DuanLangParser.ExprContext,0)


        def DOT(self):
            return self.getToken(DuanLangParser.DOT, 0)

        def getRuleIndex(self):
            return DuanLangParser.RULE_varDecl

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitVarDecl" ):
                return visitor.visitVarDecl(self)
            else:
                return visitor.visitChildren(self)




    def varDecl(self):

        localctx = DuanLangParser.VarDeclContext(self, self._ctx, self.state)
        self.enterRule(localctx, 48, self.RULE_varDecl)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 400
            self.match(DuanLangParser.K_DEFINE)
            self.state = 401
            self.match(DuanLangParser.ID)
            self.state = 404
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==DuanLangParser.K_EQUAL:
                self.state = 402
                self.match(DuanLangParser.K_EQUAL)
                self.state = 403
                self.expr()


            self.state = 407
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==DuanLangParser.DOT:
                self.state = 406
                self.match(DuanLangParser.DOT)


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class AssignStmtContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def target(self):
            return self.getTypedRuleContext(DuanLangParser.TargetContext,0)


        def K_EQUAL(self):
            return self.getToken(DuanLangParser.K_EQUAL, 0)

        def expr(self):
            return self.getTypedRuleContext(DuanLangParser.ExprContext,0)


        def DOT(self):
            return self.getToken(DuanLangParser.DOT, 0)

        def getRuleIndex(self):
            return DuanLangParser.RULE_assignStmt

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAssignStmt" ):
                return visitor.visitAssignStmt(self)
            else:
                return visitor.visitChildren(self)




    def assignStmt(self):

        localctx = DuanLangParser.AssignStmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 50, self.RULE_assignStmt)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 409
            self.target()
            self.state = 410
            self.match(DuanLangParser.K_EQUAL)
            self.state = 411
            self.expr()
            self.state = 413
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==DuanLangParser.DOT:
                self.state = 412
                self.match(DuanLangParser.DOT)


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class TargetContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ID(self):
            return self.getToken(DuanLangParser.ID, 0)

        def expr(self):
            return self.getTypedRuleContext(DuanLangParser.ExprContext,0)


        def K_OF(self):
            return self.getToken(DuanLangParser.K_OF, 0)

        def getRuleIndex(self):
            return DuanLangParser.RULE_target

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitTarget" ):
                return visitor.visitTarget(self)
            else:
                return visitor.visitChildren(self)




    def target(self):

        localctx = DuanLangParser.TargetContext(self, self._ctx, self.state)
        self.enterRule(localctx, 52, self.RULE_target)
        try:
            self.state = 420
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,47,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 415
                self.match(DuanLangParser.ID)
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 416
                self.expr()
                self.state = 417
                self.match(DuanLangParser.K_OF)
                self.state = 418
                self.match(DuanLangParser.ID)
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class IfStmtContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def K_IF(self):
            return self.getToken(DuanLangParser.K_IF, 0)

        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(DuanLangParser.ExprContext)
            else:
                return self.getTypedRuleContext(DuanLangParser.ExprContext,i)


        def K_THEN(self, i:int=None):
            if i is None:
                return self.getTokens(DuanLangParser.K_THEN)
            else:
                return self.getToken(DuanLangParser.K_THEN, i)

        def K_END(self):
            return self.getToken(DuanLangParser.K_END, 0)

        def COLON(self, i:int=None):
            if i is None:
                return self.getTokens(DuanLangParser.COLON)
            else:
                return self.getToken(DuanLangParser.COLON, i)

        def block(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(DuanLangParser.BlockContext)
            else:
                return self.getTypedRuleContext(DuanLangParser.BlockContext,i)


        def K_ELSE_IF(self, i:int=None):
            if i is None:
                return self.getTokens(DuanLangParser.K_ELSE_IF)
            else:
                return self.getToken(DuanLangParser.K_ELSE_IF, i)

        def K_ELSE(self):
            return self.getToken(DuanLangParser.K_ELSE, 0)

        def DOT(self):
            return self.getToken(DuanLangParser.DOT, 0)

        def getRuleIndex(self):
            return DuanLangParser.RULE_ifStmt

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitIfStmt" ):
                return visitor.visitIfStmt(self)
            else:
                return visitor.visitChildren(self)




    def ifStmt(self):

        localctx = DuanLangParser.IfStmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 54, self.RULE_ifStmt)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 422
            self.match(DuanLangParser.K_IF)
            self.state = 423
            self.expr()
            self.state = 424
            self.match(DuanLangParser.K_THEN)
            self.state = 427
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==DuanLangParser.COLON:
                self.state = 425
                self.match(DuanLangParser.COLON)
                self.state = 426
                self.block()


            self.state = 437
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==DuanLangParser.K_ELSE_IF:
                self.state = 429
                self.match(DuanLangParser.K_ELSE_IF)
                self.state = 430
                self.expr()
                self.state = 431
                self.match(DuanLangParser.K_THEN)
                self.state = 432
                self.match(DuanLangParser.COLON)
                self.state = 433
                self.block()
                self.state = 439
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 443
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==DuanLangParser.K_ELSE:
                self.state = 440
                self.match(DuanLangParser.K_ELSE)
                self.state = 441
                self.match(DuanLangParser.COLON)
                self.state = 442
                self.block()


            self.state = 445
            self.match(DuanLangParser.K_END)
            self.state = 447
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==DuanLangParser.DOT:
                self.state = 446
                self.match(DuanLangParser.DOT)


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ForeachStmtContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def K_FOREACH(self):
            return self.getToken(DuanLangParser.K_FOREACH, 0)

        def foreachVar(self):
            return self.getTypedRuleContext(DuanLangParser.ForeachVarContext,0)


        def expr(self):
            return self.getTypedRuleContext(DuanLangParser.ExprContext,0)


        def K_END(self):
            return self.getToken(DuanLangParser.K_END, 0)

        def COLON(self):
            return self.getToken(DuanLangParser.COLON, 0)

        def block(self):
            return self.getTypedRuleContext(DuanLangParser.BlockContext,0)


        def DOT(self):
            return self.getToken(DuanLangParser.DOT, 0)

        def getRuleIndex(self):
            return DuanLangParser.RULE_foreachStmt

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitForeachStmt" ):
                return visitor.visitForeachStmt(self)
            else:
                return visitor.visitChildren(self)




    def foreachStmt(self):

        localctx = DuanLangParser.ForeachStmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 56, self.RULE_foreachStmt)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 449
            self.match(DuanLangParser.K_FOREACH)
            self.state = 450
            self.foreachVar()
            self.state = 451
            self.expr()
            self.state = 454
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==DuanLangParser.COLON:
                self.state = 452
                self.match(DuanLangParser.COLON)
                self.state = 453
                self.block()


            self.state = 456
            self.match(DuanLangParser.K_END)
            self.state = 458
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==DuanLangParser.DOT:
                self.state = 457
                self.match(DuanLangParser.DOT)


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ForeachVarContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ID(self, i:int=None):
            if i is None:
                return self.getTokens(DuanLangParser.ID)
            else:
                return self.getToken(DuanLangParser.ID, i)

        def K_OF(self):
            return self.getToken(DuanLangParser.K_OF, 0)

        def COMMA(self):
            return self.getToken(DuanLangParser.COMMA, 0)

        def getRuleIndex(self):
            return DuanLangParser.RULE_foreachVar

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitForeachVar" ):
                return visitor.visitForeachVar(self)
            else:
                return visitor.visitChildren(self)




    def foreachVar(self):

        localctx = DuanLangParser.ForeachVarContext(self, self._ctx, self.state)
        self.enterRule(localctx, 58, self.RULE_foreachVar)
        try:
            self.state = 469
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,54,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 460
                self.match(DuanLangParser.ID)
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 461
                self.match(DuanLangParser.ID)
                self.state = 462
                self.match(DuanLangParser.K_OF)
                self.state = 463
                self.match(DuanLangParser.ID)
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 464
                self.match(DuanLangParser.ID)
                self.state = 465
                self.match(DuanLangParser.K_OF)
                self.state = 466
                self.match(DuanLangParser.ID)
                self.state = 467
                self.match(DuanLangParser.COMMA)
                self.state = 468
                self.match(DuanLangParser.ID)
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class WhileStmtContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def K_WHILE(self):
            return self.getToken(DuanLangParser.K_WHILE, 0)

        def expr(self):
            return self.getTypedRuleContext(DuanLangParser.ExprContext,0)


        def K_END(self):
            return self.getToken(DuanLangParser.K_END, 0)

        def COLON(self):
            return self.getToken(DuanLangParser.COLON, 0)

        def block(self):
            return self.getTypedRuleContext(DuanLangParser.BlockContext,0)


        def DOT(self):
            return self.getToken(DuanLangParser.DOT, 0)

        def getRuleIndex(self):
            return DuanLangParser.RULE_whileStmt

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitWhileStmt" ):
                return visitor.visitWhileStmt(self)
            else:
                return visitor.visitChildren(self)




    def whileStmt(self):

        localctx = DuanLangParser.WhileStmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 60, self.RULE_whileStmt)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 471
            self.match(DuanLangParser.K_WHILE)
            self.state = 472
            self.expr()
            self.state = 475
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==DuanLangParser.COLON:
                self.state = 473
                self.match(DuanLangParser.COLON)
                self.state = 474
                self.block()


            self.state = 477
            self.match(DuanLangParser.K_END)
            self.state = 479
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==DuanLangParser.DOT:
                self.state = 478
                self.match(DuanLangParser.DOT)


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ReturnStmtContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def K_RETURN(self):
            return self.getToken(DuanLangParser.K_RETURN, 0)

        def expr(self):
            return self.getTypedRuleContext(DuanLangParser.ExprContext,0)


        def DOT(self):
            return self.getToken(DuanLangParser.DOT, 0)

        def getRuleIndex(self):
            return DuanLangParser.RULE_returnStmt

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitReturnStmt" ):
                return visitor.visitReturnStmt(self)
            else:
                return visitor.visitChildren(self)




    def returnStmt(self):

        localctx = DuanLangParser.ReturnStmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 62, self.RULE_returnStmt)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 481
            self.match(DuanLangParser.K_RETURN)
            self.state = 483
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,57,self._ctx)
            if la_ == 1:
                self.state = 482
                self.expr()


            self.state = 486
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==DuanLangParser.DOT:
                self.state = 485
                self.match(DuanLangParser.DOT)


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class BreakStmtContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def K_BREAK(self):
            return self.getToken(DuanLangParser.K_BREAK, 0)

        def DOT(self):
            return self.getToken(DuanLangParser.DOT, 0)

        def getRuleIndex(self):
            return DuanLangParser.RULE_breakStmt

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitBreakStmt" ):
                return visitor.visitBreakStmt(self)
            else:
                return visitor.visitChildren(self)




    def breakStmt(self):

        localctx = DuanLangParser.BreakStmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 64, self.RULE_breakStmt)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 488
            self.match(DuanLangParser.K_BREAK)
            self.state = 490
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==DuanLangParser.DOT:
                self.state = 489
                self.match(DuanLangParser.DOT)


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ContinueStmtContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def K_CONTINUE(self):
            return self.getToken(DuanLangParser.K_CONTINUE, 0)

        def DOT(self):
            return self.getToken(DuanLangParser.DOT, 0)

        def getRuleIndex(self):
            return DuanLangParser.RULE_continueStmt

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitContinueStmt" ):
                return visitor.visitContinueStmt(self)
            else:
                return visitor.visitChildren(self)




    def continueStmt(self):

        localctx = DuanLangParser.ContinueStmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 66, self.RULE_continueStmt)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 492
            self.match(DuanLangParser.K_CONTINUE)
            self.state = 494
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==DuanLangParser.DOT:
                self.state = 493
                self.match(DuanLangParser.DOT)


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class TryStmtContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def K_TRY(self):
            return self.getToken(DuanLangParser.K_TRY, 0)

        def COLON(self, i:int=None):
            if i is None:
                return self.getTokens(DuanLangParser.COLON)
            else:
                return self.getToken(DuanLangParser.COLON, i)

        def block(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(DuanLangParser.BlockContext)
            else:
                return self.getTypedRuleContext(DuanLangParser.BlockContext,i)


        def K_CATCH(self):
            return self.getToken(DuanLangParser.K_CATCH, 0)

        def ID(self):
            return self.getToken(DuanLangParser.ID, 0)

        def K_END(self):
            return self.getToken(DuanLangParser.K_END, 0)

        def DOT(self):
            return self.getToken(DuanLangParser.DOT, 0)

        def getRuleIndex(self):
            return DuanLangParser.RULE_tryStmt

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitTryStmt" ):
                return visitor.visitTryStmt(self)
            else:
                return visitor.visitChildren(self)




    def tryStmt(self):

        localctx = DuanLangParser.TryStmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 68, self.RULE_tryStmt)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 496
            self.match(DuanLangParser.K_TRY)
            self.state = 497
            self.match(DuanLangParser.COLON)
            self.state = 498
            self.block()
            self.state = 499
            self.match(DuanLangParser.K_CATCH)
            self.state = 500
            self.match(DuanLangParser.ID)
            self.state = 501
            self.match(DuanLangParser.COLON)
            self.state = 502
            self.block()
            self.state = 503
            self.match(DuanLangParser.K_END)
            self.state = 505
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==DuanLangParser.DOT:
                self.state = 504
                self.match(DuanLangParser.DOT)


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ThrowStmtContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def K_THROW(self):
            return self.getToken(DuanLangParser.K_THROW, 0)

        def expr(self):
            return self.getTypedRuleContext(DuanLangParser.ExprContext,0)


        def DOT(self):
            return self.getToken(DuanLangParser.DOT, 0)

        def getRuleIndex(self):
            return DuanLangParser.RULE_throwStmt

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitThrowStmt" ):
                return visitor.visitThrowStmt(self)
            else:
                return visitor.visitChildren(self)




    def throwStmt(self):

        localctx = DuanLangParser.ThrowStmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 70, self.RULE_throwStmt)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 507
            self.match(DuanLangParser.K_THROW)
            self.state = 508
            self.expr()
            self.state = 510
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==DuanLangParser.DOT:
                self.state = 509
                self.match(DuanLangParser.DOT)


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class PrintStmtContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def expr(self):
            return self.getTypedRuleContext(DuanLangParser.ExprContext,0)


        def K_PRINT(self):
            return self.getToken(DuanLangParser.K_PRINT, 0)

        def K_OUTPUT(self):
            return self.getToken(DuanLangParser.K_OUTPUT, 0)

        def DOT(self):
            return self.getToken(DuanLangParser.DOT, 0)

        def getRuleIndex(self):
            return DuanLangParser.RULE_printStmt

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitPrintStmt" ):
                return visitor.visitPrintStmt(self)
            else:
                return visitor.visitChildren(self)




    def printStmt(self):

        localctx = DuanLangParser.PrintStmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 72, self.RULE_printStmt)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 512
            _la = self._input.LA(1)
            if not(_la==DuanLangParser.K_PRINT or _la==DuanLangParser.K_OUTPUT):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
            self.state = 513
            self.expr()
            self.state = 515
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==DuanLangParser.DOT:
                self.state = 514
                self.match(DuanLangParser.DOT)


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ExprStmtContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def expr(self):
            return self.getTypedRuleContext(DuanLangParser.ExprContext,0)


        def DOT(self):
            return self.getToken(DuanLangParser.DOT, 0)

        def getRuleIndex(self):
            return DuanLangParser.RULE_exprStmt

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitExprStmt" ):
                return visitor.visitExprStmt(self)
            else:
                return visitor.visitChildren(self)




    def exprStmt(self):

        localctx = DuanLangParser.ExprStmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 74, self.RULE_exprStmt)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 517
            self.expr()
            self.state = 519
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==DuanLangParser.DOT:
                self.state = 518
                self.match(DuanLangParser.DOT)


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ExprContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def pipelineExpr(self):
            return self.getTypedRuleContext(DuanLangParser.PipelineExprContext,0)


        def getRuleIndex(self):
            return DuanLangParser.RULE_expr

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitExpr" ):
                return visitor.visitExpr(self)
            else:
                return visitor.visitChildren(self)




    def expr(self):

        localctx = DuanLangParser.ExprContext(self, self._ctx, self.state)
        self.enterRule(localctx, 76, self.RULE_expr)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 521
            self.pipelineExpr()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class PipelineExprContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def andExpr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(DuanLangParser.AndExprContext)
            else:
                return self.getTypedRuleContext(DuanLangParser.AndExprContext,i)


        def PIPE(self, i:int=None):
            if i is None:
                return self.getTokens(DuanLangParser.PIPE)
            else:
                return self.getToken(DuanLangParser.PIPE, i)

        def K_AND_WORD(self, i:int=None):
            if i is None:
                return self.getTokens(DuanLangParser.K_AND_WORD)
            else:
                return self.getToken(DuanLangParser.K_AND_WORD, i)

        def getRuleIndex(self):
            return DuanLangParser.RULE_pipelineExpr

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitPipelineExpr" ):
                return visitor.visitPipelineExpr(self)
            else:
                return visitor.visitChildren(self)




    def pipelineExpr(self):

        localctx = DuanLangParser.PipelineExprContext(self, self._ctx, self.state)
        self.enterRule(localctx, 78, self.RULE_pipelineExpr)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 523
            self.andExpr()
            self.state = 528
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==DuanLangParser.K_AND_WORD or _la==DuanLangParser.PIPE:
                self.state = 524
                _la = self._input.LA(1)
                if not(_la==DuanLangParser.K_AND_WORD or _la==DuanLangParser.PIPE):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 525
                self.andExpr()
                self.state = 530
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class AndExprContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def orExpr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(DuanLangParser.OrExprContext)
            else:
                return self.getTypedRuleContext(DuanLangParser.OrExprContext,i)


        def K_AND(self, i:int=None):
            if i is None:
                return self.getTokens(DuanLangParser.K_AND)
            else:
                return self.getToken(DuanLangParser.K_AND, i)

        def getRuleIndex(self):
            return DuanLangParser.RULE_andExpr

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAndExpr" ):
                return visitor.visitAndExpr(self)
            else:
                return visitor.visitChildren(self)




    def andExpr(self):

        localctx = DuanLangParser.AndExprContext(self, self._ctx, self.state)
        self.enterRule(localctx, 80, self.RULE_andExpr)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 531
            self.orExpr()
            self.state = 536
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==DuanLangParser.K_AND:
                self.state = 532
                self.match(DuanLangParser.K_AND)
                self.state = 533
                self.orExpr()
                self.state = 538
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class OrExprContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def comparisonExpr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(DuanLangParser.ComparisonExprContext)
            else:
                return self.getTypedRuleContext(DuanLangParser.ComparisonExprContext,i)


        def K_OR(self, i:int=None):
            if i is None:
                return self.getTokens(DuanLangParser.K_OR)
            else:
                return self.getToken(DuanLangParser.K_OR, i)

        def getRuleIndex(self):
            return DuanLangParser.RULE_orExpr

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitOrExpr" ):
                return visitor.visitOrExpr(self)
            else:
                return visitor.visitChildren(self)




    def orExpr(self):

        localctx = DuanLangParser.OrExprContext(self, self._ctx, self.state)
        self.enterRule(localctx, 82, self.RULE_orExpr)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 539
            self.comparisonExpr()
            self.state = 544
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==DuanLangParser.K_OR:
                self.state = 540
                self.match(DuanLangParser.K_OR)
                self.state = 541
                self.comparisonExpr()
                self.state = 546
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ComparisonExprContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def additiveExpr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(DuanLangParser.AdditiveExprContext)
            else:
                return self.getTypedRuleContext(DuanLangParser.AdditiveExprContext,i)


        def compOp(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(DuanLangParser.CompOpContext)
            else:
                return self.getTypedRuleContext(DuanLangParser.CompOpContext,i)


        def getRuleIndex(self):
            return DuanLangParser.RULE_comparisonExpr

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitComparisonExpr" ):
                return visitor.visitComparisonExpr(self)
            else:
                return visitor.visitChildren(self)




    def comparisonExpr(self):

        localctx = DuanLangParser.ComparisonExprContext(self, self._ctx, self.state)
        self.enterRule(localctx, 84, self.RULE_comparisonExpr)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 547
            self.additiveExpr()
            self.state = 553
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << DuanLangParser.K_GE) | (1 << DuanLangParser.K_LE) | (1 << DuanLangParser.K_NE) | (1 << DuanLangParser.K_GT) | (1 << DuanLangParser.K_LT) | (1 << DuanLangParser.K_EQUAL))) != 0) or ((((_la - 71)) & ~0x3f) == 0 and ((1 << (_la - 71)) & ((1 << (DuanLangParser.EQ - 71)) | (1 << (DuanLangParser.NE - 71)) | (1 << (DuanLangParser.GE - 71)) | (1 << (DuanLangParser.LE - 71)) | (1 << (DuanLangParser.GT - 71)) | (1 << (DuanLangParser.LT - 71)))) != 0):
                self.state = 548
                self.compOp()
                self.state = 549
                self.additiveExpr()
                self.state = 555
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class CompOpContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def K_GE(self):
            return self.getToken(DuanLangParser.K_GE, 0)

        def K_LE(self):
            return self.getToken(DuanLangParser.K_LE, 0)

        def K_GT(self):
            return self.getToken(DuanLangParser.K_GT, 0)

        def K_LT(self):
            return self.getToken(DuanLangParser.K_LT, 0)

        def K_NE(self):
            return self.getToken(DuanLangParser.K_NE, 0)

        def K_EQUAL(self):
            return self.getToken(DuanLangParser.K_EQUAL, 0)

        def GE(self):
            return self.getToken(DuanLangParser.GE, 0)

        def LE(self):
            return self.getToken(DuanLangParser.LE, 0)

        def GT(self):
            return self.getToken(DuanLangParser.GT, 0)

        def LT(self):
            return self.getToken(DuanLangParser.LT, 0)

        def NE(self):
            return self.getToken(DuanLangParser.NE, 0)

        def EQ(self):
            return self.getToken(DuanLangParser.EQ, 0)

        def getRuleIndex(self):
            return DuanLangParser.RULE_compOp

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitCompOp" ):
                return visitor.visitCompOp(self)
            else:
                return visitor.visitChildren(self)




    def compOp(self):

        localctx = DuanLangParser.CompOpContext(self, self._ctx, self.state)
        self.enterRule(localctx, 86, self.RULE_compOp)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 556
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << DuanLangParser.K_GE) | (1 << DuanLangParser.K_LE) | (1 << DuanLangParser.K_NE) | (1 << DuanLangParser.K_GT) | (1 << DuanLangParser.K_LT) | (1 << DuanLangParser.K_EQUAL))) != 0) or ((((_la - 71)) & ~0x3f) == 0 and ((1 << (_la - 71)) & ((1 << (DuanLangParser.EQ - 71)) | (1 << (DuanLangParser.NE - 71)) | (1 << (DuanLangParser.GE - 71)) | (1 << (DuanLangParser.LE - 71)) | (1 << (DuanLangParser.GT - 71)) | (1 << (DuanLangParser.LT - 71)))) != 0)):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class AdditiveExprContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def multiplicativeExpr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(DuanLangParser.MultiplicativeExprContext)
            else:
                return self.getTypedRuleContext(DuanLangParser.MultiplicativeExprContext,i)


        def addOp(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(DuanLangParser.AddOpContext)
            else:
                return self.getTypedRuleContext(DuanLangParser.AddOpContext,i)


        def getRuleIndex(self):
            return DuanLangParser.RULE_additiveExpr

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAdditiveExpr" ):
                return visitor.visitAdditiveExpr(self)
            else:
                return visitor.visitChildren(self)




    def additiveExpr(self):

        localctx = DuanLangParser.AdditiveExprContext(self, self._ctx, self.state)
        self.enterRule(localctx, 88, self.RULE_additiveExpr)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 558
            self.multiplicativeExpr()
            self.state = 564
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,69,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 559
                    self.addOp()
                    self.state = 560
                    self.multiplicativeExpr() 
                self.state = 566
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,69,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class AddOpContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def K_PLUS(self):
            return self.getToken(DuanLangParser.K_PLUS, 0)

        def K_MINUS(self):
            return self.getToken(DuanLangParser.K_MINUS, 0)

        def PLUS(self):
            return self.getToken(DuanLangParser.PLUS, 0)

        def MINUS(self):
            return self.getToken(DuanLangParser.MINUS, 0)

        def getRuleIndex(self):
            return DuanLangParser.RULE_addOp

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAddOp" ):
                return visitor.visitAddOp(self)
            else:
                return visitor.visitChildren(self)




    def addOp(self):

        localctx = DuanLangParser.AddOpContext(self, self._ctx, self.state)
        self.enterRule(localctx, 90, self.RULE_addOp)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 567
            _la = self._input.LA(1)
            if not(((((_la - 44)) & ~0x3f) == 0 and ((1 << (_la - 44)) & ((1 << (DuanLangParser.K_PLUS - 44)) | (1 << (DuanLangParser.K_MINUS - 44)) | (1 << (DuanLangParser.PLUS - 44)) | (1 << (DuanLangParser.MINUS - 44)))) != 0)):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class MultiplicativeExprContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def unaryExpr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(DuanLangParser.UnaryExprContext)
            else:
                return self.getTypedRuleContext(DuanLangParser.UnaryExprContext,i)


        def multOp(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(DuanLangParser.MultOpContext)
            else:
                return self.getTypedRuleContext(DuanLangParser.MultOpContext,i)


        def getRuleIndex(self):
            return DuanLangParser.RULE_multiplicativeExpr

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitMultiplicativeExpr" ):
                return visitor.visitMultiplicativeExpr(self)
            else:
                return visitor.visitChildren(self)




    def multiplicativeExpr(self):

        localctx = DuanLangParser.MultiplicativeExprContext(self, self._ctx, self.state)
        self.enterRule(localctx, 92, self.RULE_multiplicativeExpr)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 569
            self.unaryExpr()
            self.state = 575
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while ((((_la - 46)) & ~0x3f) == 0 and ((1 << (_la - 46)) & ((1 << (DuanLangParser.K_MULTIPLY - 46)) | (1 << (DuanLangParser.K_DIVIDE - 46)) | (1 << (DuanLangParser.K_MOD - 46)) | (1 << (DuanLangParser.K_POW - 46)) | (1 << (DuanLangParser.POW - 46)) | (1 << (DuanLangParser.MODULO - 46)) | (1 << (DuanLangParser.MULTIPLY - 46)) | (1 << (DuanLangParser.DIVIDE - 46)))) != 0):
                self.state = 570
                self.multOp()
                self.state = 571
                self.unaryExpr()
                self.state = 577
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class MultOpContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def K_MULTIPLY(self):
            return self.getToken(DuanLangParser.K_MULTIPLY, 0)

        def K_DIVIDE(self):
            return self.getToken(DuanLangParser.K_DIVIDE, 0)

        def K_MOD(self):
            return self.getToken(DuanLangParser.K_MOD, 0)

        def K_POW(self):
            return self.getToken(DuanLangParser.K_POW, 0)

        def MULTIPLY(self):
            return self.getToken(DuanLangParser.MULTIPLY, 0)

        def DIVIDE(self):
            return self.getToken(DuanLangParser.DIVIDE, 0)

        def MODULO(self):
            return self.getToken(DuanLangParser.MODULO, 0)

        def POW(self):
            return self.getToken(DuanLangParser.POW, 0)

        def getRuleIndex(self):
            return DuanLangParser.RULE_multOp

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitMultOp" ):
                return visitor.visitMultOp(self)
            else:
                return visitor.visitChildren(self)




    def multOp(self):

        localctx = DuanLangParser.MultOpContext(self, self._ctx, self.state)
        self.enterRule(localctx, 94, self.RULE_multOp)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 578
            _la = self._input.LA(1)
            if not(((((_la - 46)) & ~0x3f) == 0 and ((1 << (_la - 46)) & ((1 << (DuanLangParser.K_MULTIPLY - 46)) | (1 << (DuanLangParser.K_DIVIDE - 46)) | (1 << (DuanLangParser.K_MOD - 46)) | (1 << (DuanLangParser.K_POW - 46)) | (1 << (DuanLangParser.POW - 46)) | (1 << (DuanLangParser.MODULO - 46)) | (1 << (DuanLangParser.MULTIPLY - 46)) | (1 << (DuanLangParser.DIVIDE - 46)))) != 0)):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class UnaryExprContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def unaryExpr(self):
            return self.getTypedRuleContext(DuanLangParser.UnaryExprContext,0)


        def K_NOT(self):
            return self.getToken(DuanLangParser.K_NOT, 0)

        def NOT(self):
            return self.getToken(DuanLangParser.NOT, 0)

        def MINUS(self):
            return self.getToken(DuanLangParser.MINUS, 0)

        def K_MINUS(self):
            return self.getToken(DuanLangParser.K_MINUS, 0)

        def postfixExpr(self):
            return self.getTypedRuleContext(DuanLangParser.PostfixExprContext,0)


        def getRuleIndex(self):
            return DuanLangParser.RULE_unaryExpr

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitUnaryExpr" ):
                return visitor.visitUnaryExpr(self)
            else:
                return visitor.visitChildren(self)




    def unaryExpr(self):

        localctx = DuanLangParser.UnaryExprContext(self, self._ctx, self.state)
        self.enterRule(localctx, 96, self.RULE_unaryExpr)
        self._la = 0 # Token type
        try:
            self.state = 585
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [DuanLangParser.K_NOT, DuanLangParser.NOT]:
                self.enterOuterAlt(localctx, 1)
                self.state = 580
                _la = self._input.LA(1)
                if not(_la==DuanLangParser.K_NOT or _la==DuanLangParser.NOT):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 581
                self.unaryExpr()
                pass
            elif token in [DuanLangParser.K_MINUS, DuanLangParser.MINUS]:
                self.enterOuterAlt(localctx, 2)
                self.state = 582
                _la = self._input.LA(1)
                if not(_la==DuanLangParser.K_MINUS or _la==DuanLangParser.MINUS):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 583
                self.unaryExpr()
                pass
            elif token in [DuanLangParser.K_NEW, DuanLangParser.K_TRUE, DuanLangParser.K_FALSE, DuanLangParser.K_NULL, DuanLangParser.LPAREN, DuanLangParser.LBRACKET, DuanLangParser.BOOK_L, DuanLangParser.NUMBER, DuanLangParser.STRING, DuanLangParser.ID]:
                self.enterOuterAlt(localctx, 3)
                self.state = 584
                self.postfixExpr()
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class PostfixExprContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def primary(self):
            return self.getTypedRuleContext(DuanLangParser.PrimaryContext,0)


        def BOOK_L(self, i:int=None):
            if i is None:
                return self.getTokens(DuanLangParser.BOOK_L)
            else:
                return self.getToken(DuanLangParser.BOOK_L, i)

        def ID(self, i:int=None):
            if i is None:
                return self.getTokens(DuanLangParser.ID)
            else:
                return self.getToken(DuanLangParser.ID, i)

        def BOOK_R(self, i:int=None):
            if i is None:
                return self.getTokens(DuanLangParser.BOOK_R)
            else:
                return self.getToken(DuanLangParser.BOOK_R, i)

        def LPAREN(self, i:int=None):
            if i is None:
                return self.getTokens(DuanLangParser.LPAREN)
            else:
                return self.getToken(DuanLangParser.LPAREN, i)

        def RPAREN(self, i:int=None):
            if i is None:
                return self.getTokens(DuanLangParser.RPAREN)
            else:
                return self.getToken(DuanLangParser.RPAREN, i)

        def K_OF(self, i:int=None):
            if i is None:
                return self.getTokens(DuanLangParser.K_OF)
            else:
                return self.getToken(DuanLangParser.K_OF, i)

        def LBRACKET(self, i:int=None):
            if i is None:
                return self.getTokens(DuanLangParser.LBRACKET)
            else:
                return self.getToken(DuanLangParser.LBRACKET, i)

        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(DuanLangParser.ExprContext)
            else:
                return self.getTypedRuleContext(DuanLangParser.ExprContext,i)


        def RBRACKET(self, i:int=None):
            if i is None:
                return self.getTokens(DuanLangParser.RBRACKET)
            else:
                return self.getToken(DuanLangParser.RBRACKET, i)

        def exprList(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(DuanLangParser.ExprListContext)
            else:
                return self.getTypedRuleContext(DuanLangParser.ExprListContext,i)


        def getRuleIndex(self):
            return DuanLangParser.RULE_postfixExpr

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitPostfixExpr" ):
                return visitor.visitPostfixExpr(self)
            else:
                return visitor.visitChildren(self)




    def postfixExpr(self):

        localctx = DuanLangParser.PostfixExprContext(self, self._ctx, self.state)
        self.enterRule(localctx, 98, self.RULE_postfixExpr)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 587
            self.primary()
            self.state = 609
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,75,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 607
                    self._errHandler.sync(self)
                    token = self._input.LA(1)
                    if token in [DuanLangParser.BOOK_L]:
                        self.state = 588
                        self.match(DuanLangParser.BOOK_L)
                        self.state = 589
                        self.match(DuanLangParser.ID)
                        self.state = 590
                        self.match(DuanLangParser.BOOK_R)
                        self.state = 591
                        self.match(DuanLangParser.LPAREN)
                        self.state = 593
                        self._errHandler.sync(self)
                        _la = self._input.LA(1)
                        if (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << DuanLangParser.K_NEW) | (1 << DuanLangParser.K_NOT) | (1 << DuanLangParser.K_MINUS) | (1 << DuanLangParser.K_TRUE) | (1 << DuanLangParser.K_FALSE) | (1 << DuanLangParser.K_NULL))) != 0) or ((((_la - 70)) & ~0x3f) == 0 and ((1 << (_la - 70)) & ((1 << (DuanLangParser.MINUS - 70)) | (1 << (DuanLangParser.NOT - 70)) | (1 << (DuanLangParser.LPAREN - 70)) | (1 << (DuanLangParser.LBRACKET - 70)) | (1 << (DuanLangParser.BOOK_L - 70)) | (1 << (DuanLangParser.NUMBER - 70)) | (1 << (DuanLangParser.STRING - 70)) | (1 << (DuanLangParser.ID - 70)))) != 0):
                            self.state = 592
                            self.exprList()


                        self.state = 595
                        self.match(DuanLangParser.RPAREN)
                        pass
                    elif token in [DuanLangParser.LPAREN]:
                        self.state = 596
                        self.match(DuanLangParser.LPAREN)
                        self.state = 598
                        self._errHandler.sync(self)
                        _la = self._input.LA(1)
                        if (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << DuanLangParser.K_NEW) | (1 << DuanLangParser.K_NOT) | (1 << DuanLangParser.K_MINUS) | (1 << DuanLangParser.K_TRUE) | (1 << DuanLangParser.K_FALSE) | (1 << DuanLangParser.K_NULL))) != 0) or ((((_la - 70)) & ~0x3f) == 0 and ((1 << (_la - 70)) & ((1 << (DuanLangParser.MINUS - 70)) | (1 << (DuanLangParser.NOT - 70)) | (1 << (DuanLangParser.LPAREN - 70)) | (1 << (DuanLangParser.LBRACKET - 70)) | (1 << (DuanLangParser.BOOK_L - 70)) | (1 << (DuanLangParser.NUMBER - 70)) | (1 << (DuanLangParser.STRING - 70)) | (1 << (DuanLangParser.ID - 70)))) != 0):
                            self.state = 597
                            self.exprList()


                        self.state = 600
                        self.match(DuanLangParser.RPAREN)
                        pass
                    elif token in [DuanLangParser.K_OF]:
                        self.state = 601
                        self.match(DuanLangParser.K_OF)
                        self.state = 602
                        self.match(DuanLangParser.ID)
                        pass
                    elif token in [DuanLangParser.LBRACKET]:
                        self.state = 603
                        self.match(DuanLangParser.LBRACKET)
                        self.state = 604
                        self.expr()
                        self.state = 605
                        self.match(DuanLangParser.RBRACKET)
                        pass
                    else:
                        raise NoViableAltException(self)
             
                self.state = 611
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,75,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class PrimaryContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def NUMBER(self):
            return self.getToken(DuanLangParser.NUMBER, 0)

        def STRING(self):
            return self.getToken(DuanLangParser.STRING, 0)

        def K_TRUE(self):
            return self.getToken(DuanLangParser.K_TRUE, 0)

        def K_FALSE(self):
            return self.getToken(DuanLangParser.K_FALSE, 0)

        def K_NULL(self):
            return self.getToken(DuanLangParser.K_NULL, 0)

        def ID(self):
            return self.getToken(DuanLangParser.ID, 0)

        def LPAREN(self):
            return self.getToken(DuanLangParser.LPAREN, 0)

        def expr(self):
            return self.getTypedRuleContext(DuanLangParser.ExprContext,0)


        def RPAREN(self):
            return self.getToken(DuanLangParser.RPAREN, 0)

        def LBRACKET(self):
            return self.getToken(DuanLangParser.LBRACKET, 0)

        def dictLiteral(self):
            return self.getTypedRuleContext(DuanLangParser.DictLiteralContext,0)


        def RBRACKET(self):
            return self.getToken(DuanLangParser.RBRACKET, 0)

        def exprList(self):
            return self.getTypedRuleContext(DuanLangParser.ExprListContext,0)


        def BOOK_L(self):
            return self.getToken(DuanLangParser.BOOK_L, 0)

        def BOOK_R(self):
            return self.getToken(DuanLangParser.BOOK_R, 0)

        def K_NEW(self):
            return self.getToken(DuanLangParser.K_NEW, 0)

        def getRuleIndex(self):
            return DuanLangParser.RULE_primary

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitPrimary" ):
                return visitor.visitPrimary(self)
            else:
                return visitor.visitChildren(self)




    def primary(self):

        localctx = DuanLangParser.PrimaryContext(self, self._ctx, self.state)
        self.enterRule(localctx, 100, self.RULE_primary)
        self._la = 0 # Token type
        try:
            self.state = 641
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,78,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 612
                self.match(DuanLangParser.NUMBER)
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 613
                self.match(DuanLangParser.STRING)
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 614
                self.match(DuanLangParser.K_TRUE)
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 615
                self.match(DuanLangParser.K_FALSE)
                pass

            elif la_ == 5:
                self.enterOuterAlt(localctx, 5)
                self.state = 616
                self.match(DuanLangParser.K_NULL)
                pass

            elif la_ == 6:
                self.enterOuterAlt(localctx, 6)
                self.state = 617
                self.match(DuanLangParser.ID)
                pass

            elif la_ == 7:
                self.enterOuterAlt(localctx, 7)
                self.state = 618
                self.match(DuanLangParser.LPAREN)
                self.state = 619
                self.expr()
                self.state = 620
                self.match(DuanLangParser.RPAREN)
                pass

            elif la_ == 8:
                self.enterOuterAlt(localctx, 8)
                self.state = 622
                self.match(DuanLangParser.LBRACKET)
                self.state = 623
                self.dictLiteral()
                self.state = 624
                self.match(DuanLangParser.RBRACKET)
                pass

            elif la_ == 9:
                self.enterOuterAlt(localctx, 9)
                self.state = 626
                self.match(DuanLangParser.LBRACKET)
                self.state = 628
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << DuanLangParser.K_NEW) | (1 << DuanLangParser.K_NOT) | (1 << DuanLangParser.K_MINUS) | (1 << DuanLangParser.K_TRUE) | (1 << DuanLangParser.K_FALSE) | (1 << DuanLangParser.K_NULL))) != 0) or ((((_la - 70)) & ~0x3f) == 0 and ((1 << (_la - 70)) & ((1 << (DuanLangParser.MINUS - 70)) | (1 << (DuanLangParser.NOT - 70)) | (1 << (DuanLangParser.LPAREN - 70)) | (1 << (DuanLangParser.LBRACKET - 70)) | (1 << (DuanLangParser.BOOK_L - 70)) | (1 << (DuanLangParser.NUMBER - 70)) | (1 << (DuanLangParser.STRING - 70)) | (1 << (DuanLangParser.ID - 70)))) != 0):
                    self.state = 627
                    self.exprList()


                self.state = 630
                self.match(DuanLangParser.RBRACKET)
                pass

            elif la_ == 10:
                self.enterOuterAlt(localctx, 10)
                self.state = 631
                self.match(DuanLangParser.BOOK_L)
                self.state = 632
                self.match(DuanLangParser.ID)
                self.state = 633
                self.match(DuanLangParser.BOOK_R)
                pass

            elif la_ == 11:
                self.enterOuterAlt(localctx, 11)
                self.state = 634
                self.match(DuanLangParser.K_NEW)
                self.state = 635
                self.match(DuanLangParser.ID)
                self.state = 636
                self.match(DuanLangParser.LPAREN)
                self.state = 638
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << DuanLangParser.K_NEW) | (1 << DuanLangParser.K_NOT) | (1 << DuanLangParser.K_MINUS) | (1 << DuanLangParser.K_TRUE) | (1 << DuanLangParser.K_FALSE) | (1 << DuanLangParser.K_NULL))) != 0) or ((((_la - 70)) & ~0x3f) == 0 and ((1 << (_la - 70)) & ((1 << (DuanLangParser.MINUS - 70)) | (1 << (DuanLangParser.NOT - 70)) | (1 << (DuanLangParser.LPAREN - 70)) | (1 << (DuanLangParser.LBRACKET - 70)) | (1 << (DuanLangParser.BOOK_L - 70)) | (1 << (DuanLangParser.NUMBER - 70)) | (1 << (DuanLangParser.STRING - 70)) | (1 << (DuanLangParser.ID - 70)))) != 0):
                    self.state = 637
                    self.exprList()


                self.state = 640
                self.match(DuanLangParser.RPAREN)
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class DictLiteralContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def dictEntry(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(DuanLangParser.DictEntryContext)
            else:
                return self.getTypedRuleContext(DuanLangParser.DictEntryContext,i)


        def COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(DuanLangParser.COMMA)
            else:
                return self.getToken(DuanLangParser.COMMA, i)

        def getRuleIndex(self):
            return DuanLangParser.RULE_dictLiteral

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitDictLiteral" ):
                return visitor.visitDictLiteral(self)
            else:
                return visitor.visitChildren(self)




    def dictLiteral(self):

        localctx = DuanLangParser.DictLiteralContext(self, self._ctx, self.state)
        self.enterRule(localctx, 102, self.RULE_dictLiteral)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 643
            self.dictEntry()
            self.state = 648
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==DuanLangParser.COMMA:
                self.state = 644
                self.match(DuanLangParser.COMMA)
                self.state = 645
                self.dictEntry()
                self.state = 650
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class DictEntryContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(DuanLangParser.ExprContext)
            else:
                return self.getTypedRuleContext(DuanLangParser.ExprContext,i)


        def COLON(self):
            return self.getToken(DuanLangParser.COLON, 0)

        def getRuleIndex(self):
            return DuanLangParser.RULE_dictEntry

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitDictEntry" ):
                return visitor.visitDictEntry(self)
            else:
                return visitor.visitChildren(self)




    def dictEntry(self):

        localctx = DuanLangParser.DictEntryContext(self, self._ctx, self.state)
        self.enterRule(localctx, 104, self.RULE_dictEntry)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 651
            self.expr()
            self.state = 652
            self.match(DuanLangParser.COLON)
            self.state = 653
            self.expr()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class TypeAnnotationContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def builtinType(self):
            return self.getTypedRuleContext(DuanLangParser.BuiltinTypeContext,0)


        def genericType(self):
            return self.getTypedRuleContext(DuanLangParser.GenericTypeContext,0)


        def ID(self):
            return self.getToken(DuanLangParser.ID, 0)

        def getRuleIndex(self):
            return DuanLangParser.RULE_typeAnnotation

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitTypeAnnotation" ):
                return visitor.visitTypeAnnotation(self)
            else:
                return visitor.visitChildren(self)




    def typeAnnotation(self):

        localctx = DuanLangParser.TypeAnnotationContext(self, self._ctx, self.state)
        self.enterRule(localctx, 106, self.RULE_typeAnnotation)
        try:
            self.state = 658
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,80,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 655
                self.builtinType()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 656
                self.genericType()
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 657
                self.match(DuanLangParser.ID)
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class GenericTypeContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ID(self):
            return self.getToken(DuanLangParser.ID, 0)

        def LBRACKET(self):
            return self.getToken(DuanLangParser.LBRACKET, 0)

        def typeAnnotation(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(DuanLangParser.TypeAnnotationContext)
            else:
                return self.getTypedRuleContext(DuanLangParser.TypeAnnotationContext,i)


        def RBRACKET(self):
            return self.getToken(DuanLangParser.RBRACKET, 0)

        def COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(DuanLangParser.COMMA)
            else:
                return self.getToken(DuanLangParser.COMMA, i)

        def getRuleIndex(self):
            return DuanLangParser.RULE_genericType

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitGenericType" ):
                return visitor.visitGenericType(self)
            else:
                return visitor.visitChildren(self)




    def genericType(self):

        localctx = DuanLangParser.GenericTypeContext(self, self._ctx, self.state)
        self.enterRule(localctx, 108, self.RULE_genericType)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 660
            self.match(DuanLangParser.ID)
            self.state = 661
            self.match(DuanLangParser.LBRACKET)
            self.state = 662
            self.typeAnnotation()
            self.state = 667
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==DuanLangParser.COMMA:
                self.state = 663
                self.match(DuanLangParser.COMMA)
                self.state = 664
                self.typeAnnotation()
                self.state = 669
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 670
            self.match(DuanLangParser.RBRACKET)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class BuiltinTypeContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def T_NUMBER(self):
            return self.getToken(DuanLangParser.T_NUMBER, 0)

        def T_INT(self):
            return self.getToken(DuanLangParser.T_INT, 0)

        def T_FLOAT(self):
            return self.getToken(DuanLangParser.T_FLOAT, 0)

        def T_STRING(self):
            return self.getToken(DuanLangParser.T_STRING, 0)

        def T_BOOL(self):
            return self.getToken(DuanLangParser.T_BOOL, 0)

        def K_NULL(self):
            return self.getToken(DuanLangParser.K_NULL, 0)

        def T_ANY(self):
            return self.getToken(DuanLangParser.T_ANY, 0)

        def T_LIST(self):
            return self.getToken(DuanLangParser.T_LIST, 0)

        def T_DICT(self):
            return self.getToken(DuanLangParser.T_DICT, 0)

        def T_SET(self):
            return self.getToken(DuanLangParser.T_SET, 0)

        def LBRACKET(self):
            return self.getToken(DuanLangParser.LBRACKET, 0)

        def typeAnnotation(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(DuanLangParser.TypeAnnotationContext)
            else:
                return self.getTypedRuleContext(DuanLangParser.TypeAnnotationContext,i)


        def RBRACKET(self):
            return self.getToken(DuanLangParser.RBRACKET, 0)

        def COMMA(self):
            return self.getToken(DuanLangParser.COMMA, 0)

        def getRuleIndex(self):
            return DuanLangParser.RULE_builtinType

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitBuiltinType" ):
                return visitor.visitBuiltinType(self)
            else:
                return visitor.visitChildren(self)




    def builtinType(self):

        localctx = DuanLangParser.BuiltinTypeContext(self, self._ctx, self.state)
        self.enterRule(localctx, 110, self.RULE_builtinType)
        try:
            self.state = 699
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,82,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 672
                self.match(DuanLangParser.T_NUMBER)
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 673
                self.match(DuanLangParser.T_INT)
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 674
                self.match(DuanLangParser.T_FLOAT)
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 675
                self.match(DuanLangParser.T_STRING)
                pass

            elif la_ == 5:
                self.enterOuterAlt(localctx, 5)
                self.state = 676
                self.match(DuanLangParser.T_BOOL)
                pass

            elif la_ == 6:
                self.enterOuterAlt(localctx, 6)
                self.state = 677
                self.match(DuanLangParser.K_NULL)
                pass

            elif la_ == 7:
                self.enterOuterAlt(localctx, 7)
                self.state = 678
                self.match(DuanLangParser.T_ANY)
                pass

            elif la_ == 8:
                self.enterOuterAlt(localctx, 8)
                self.state = 679
                self.match(DuanLangParser.T_LIST)
                pass

            elif la_ == 9:
                self.enterOuterAlt(localctx, 9)
                self.state = 680
                self.match(DuanLangParser.T_DICT)
                pass

            elif la_ == 10:
                self.enterOuterAlt(localctx, 10)
                self.state = 681
                self.match(DuanLangParser.T_SET)
                pass

            elif la_ == 11:
                self.enterOuterAlt(localctx, 11)
                self.state = 682
                self.match(DuanLangParser.T_LIST)
                self.state = 683
                self.match(DuanLangParser.LBRACKET)
                self.state = 684
                self.typeAnnotation()
                self.state = 685
                self.match(DuanLangParser.RBRACKET)
                pass

            elif la_ == 12:
                self.enterOuterAlt(localctx, 12)
                self.state = 687
                self.match(DuanLangParser.T_DICT)
                self.state = 688
                self.match(DuanLangParser.LBRACKET)
                self.state = 689
                self.typeAnnotation()
                self.state = 690
                self.match(DuanLangParser.COMMA)
                self.state = 691
                self.typeAnnotation()
                self.state = 692
                self.match(DuanLangParser.RBRACKET)
                pass

            elif la_ == 13:
                self.enterOuterAlt(localctx, 13)
                self.state = 694
                self.match(DuanLangParser.T_SET)
                self.state = 695
                self.match(DuanLangParser.LBRACKET)
                self.state = 696
                self.typeAnnotation()
                self.state = 697
                self.match(DuanLangParser.RBRACKET)
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ExprListContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(DuanLangParser.ExprContext)
            else:
                return self.getTypedRuleContext(DuanLangParser.ExprContext,i)


        def COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(DuanLangParser.COMMA)
            else:
                return self.getToken(DuanLangParser.COMMA, i)

        def getRuleIndex(self):
            return DuanLangParser.RULE_exprList

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitExprList" ):
                return visitor.visitExprList(self)
            else:
                return visitor.visitChildren(self)




    def exprList(self):

        localctx = DuanLangParser.ExprListContext(self, self._ctx, self.state)
        self.enterRule(localctx, 112, self.RULE_exprList)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 701
            self.expr()
            self.state = 706
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==DuanLangParser.COMMA:
                self.state = 702
                self.match(DuanLangParser.COMMA)
                self.state = 703
                self.expr()
                self.state = 708
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx





