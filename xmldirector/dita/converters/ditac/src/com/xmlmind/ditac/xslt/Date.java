/*
 * Copyright (c) 2009-2014 Pixware SARL. All rights reserved.
 *
 * Author: Hussein Shafie
 *
 * This file is part of the XMLmind DITA Converter project.
 * For conditions of distribution and use, see the accompanying LEGAL.txt file.
 */
package com.xmlmind.ditac.xslt;

import java.util.Locale;
import java.text.DateFormat;
import java.text.SimpleDateFormat;
import java.text.ParseException;

/*package*/ final class Date {
    private Date() {}

    // -----------------------------------------------------------------------

    public static String format(String value, String lang) {
        try {
            java.util.Date date;
            value = value.trim();
            if (value.length() == 0) {
                date = new java.util.Date();
            } else {
                // Date formats are not synchronized. It is recommended to
                // create separate format instances for each thread.

                SimpleDateFormat inFormat = 
                    new SimpleDateFormat("yyyy-MM-dd", Locale.US);
                inFormat.setLenient(false);

                date = inFormat.parse(value);
            }

            DateFormat outFormat = 
                DateFormat.getDateInstance(DateFormat.LONG, new Locale(lang));

            return outFormat.format(date);
        } catch (ParseException ignored) {
            return value;
        }
    }
}
