package com.manim.utils;

import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;

/**
 * MD5 加密工具类（JDK 原生实现）
 */
public class Md5Util {

    private static final char[] HEX_DIGITS =
            {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
             'a', 'b', 'c', 'd', 'e', 'f'};

    /**
     * MD5 加密
     *
     * @param input 原始字符串
     * @return 32 位小写 MD5 值
     */
    public static String md5(String input) {
        if (input == null) return null;
        try {
            MessageDigest md = MessageDigest.getInstance("MD5");
            byte[] digest = md.digest(input.getBytes());
            StringBuilder sb = new StringBuilder(32);
            for (byte b : digest) {
                sb.append(HEX_DIGITS[(b >> 4) & 0x0f]);
                sb.append(HEX_DIGITS[b & 0x0f]);
            }
            return sb.toString();
        } catch (NoSuchAlgorithmException e) {
            throw new RuntimeException("MD5 算法不可用", e);
        }
    }
}
