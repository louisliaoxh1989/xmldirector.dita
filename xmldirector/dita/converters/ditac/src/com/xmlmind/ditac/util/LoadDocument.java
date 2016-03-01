/*
 * Copyright (c) 2009-2015 Pixware SARL. All rights reserved.
 *
 * Author: Hussein Shafie
 *
 * This file is part of the XMLmind DITA Converter project.
 * For conditions of distribution and use, see the accompanying LEGAL.txt file.
 */
package com.xmlmind.ditac.util;

import java.io.IOException;
import java.io.File;
import java.io.InputStream;
import java.io.BufferedInputStream;
import java.net.URL;
import javax.xml.parsers.SAXParserFactory;
import org.xml.sax.SAXException;
import org.xml.sax.SAXParseException;
import org.xml.sax.ErrorHandler;
import org.xml.sax.XMLReader;
import org.xml.sax.InputSource;
import org.w3c.dom.Document;
import com.xmlmind.util.ThrowableUtil;
import com.xmlmind.util.FileUtil;
import com.xmlmind.util.URLUtil;
import com.xmlmind.util.Console;

public final class LoadDocument {
    private LoadDocument() {}

    // -----------------------------------------------------------------------

    private static boolean[] addElementPointer = new boolean[1];

    public static void setAddingElementPointer(boolean add) {
        synchronized (addElementPointer) {
            addElementPointer[0] = add;
        }
    }

    public static boolean isAddingElementPointer() {
        synchronized (addElementPointer) {
            return addElementPointer[0];
        }
    }

    // -----------------------------------------------------------------------

    private static SAXToDOMFactory[] saxToDOMFactory = new SAXToDOMFactory[] {
        SAXToDOMFactory.INSTANCE
    };

    public static void setSAXToDOMFactory(SAXToDOMFactory factory) {
        if (factory == null) {
            factory = SAXToDOMFactory.INSTANCE;
        }
        synchronized (saxToDOMFactory) {
            saxToDOMFactory[0] = factory;
        }
    }

    public static SAXToDOMFactory getSAXToDOMFactory() {
        synchronized (saxToDOMFactory) {
            return saxToDOMFactory[0];
        }
    }

    // -----------------------------------------------------------------------

    public static Document load(File file, boolean validate, Console console) 
        throws IOException {
        return load(FileUtil.fileToURL(file), validate, console);
    }

    public static Document load(URL url, boolean validate, Console console) 
        throws IOException {
        Document doc;
        XMLReader parser;
        try {
            doc = DOMUtil.newDocument();

            parser = createSAXParser(validate);
        } catch (Exception shouldNotHappen) {
            throw new IOException(ThrowableUtil.reason(shouldNotHappen));
        }
        
        InputStream in = 
            new BufferedInputStream(URLUtil.openStreamNoCache(url));

        InputSource input = new InputSource(in);
        input.setSystemId(url.toExternalForm());

        SAXToDOM domBuilder = 
            getSAXToDOMFactory().createSAXToDOM(doc, isAddingElementPointer());
        parser.setContentHandler(domBuilder);

        ErrorHandler errorHandler;
        if (validate) {
            // Really needed when setValidating(true). 
            errorHandler = new LoadErrorHandler(console);
        } else {
            errorHandler = domBuilder;
        }
        parser.setErrorHandler(errorHandler);

        try {
            parser.parse(input);
        } catch (SAXParseException e) {
            throw new IOException(LoadErrorHandler.format(e, null));
        } catch (SAXException e) {
            throw new IOException(ThrowableUtil.reason(e));
        } finally {
            in.close();
        }

        int errorCount;
        if (validate && 
            (errorHandler instanceof LoadErrorHandler) && 
            (errorCount=((LoadErrorHandler)errorHandler).getErrorCount()) > 0) {
            throw new IOException(Msg.msg("hasValidationErrors", 
                                          URLUtil.toLabel(url), errorCount));
        }

        doc.setDocumentURI(url.toExternalForm());
        return doc;
    }

    private static XMLReader createSAXParser(boolean validate) {
        XMLReader parser = null;

        try {
            SAXParserFactory factory = SAXParserFactory.newInstance();

            factory.setNamespaceAware(true);

            // We need attribute default values but it seems that we get
            // them even without turning validation on.
            factory.setValidating(validate);

            factory.setXIncludeAware(false);

            // We need the qNames.
            factory.setFeature(
                "http://xml.org/sax/features/namespace-prefixes", true);

            // Expand entities.
            factory.setFeature(
              "http://xml.org/sax/features/external-general-entities", true);
            factory.setFeature(
              "http://xml.org/sax/features/external-parameter-entities", true);

            factory.setFeature(
              "http://xml.org/sax/features/lexical-handler/parameter-entities",
              false);
            factory.setFeature(
              "http://xml.org/sax/features/resolve-dtd-uris", true);

            // For Xerces which otherwise, does not support "x-MacRoman".
            try {
                factory.setFeature(
                    "http://apache.org/xml/features/allow-java-encodings",
                    true);
            } catch (Exception ignored) {}

            // Without this feature, Xerces ignores
            // xsi:noNamespaceSchemaLocation.
            //
            // Now the question is: how Xerces resolves URIs such as
            // "urn:oasis:names:tc:dita:xsd:topicGrp.xsd:1.1"? 
            // Seems the EntityResolver specified below in order 
            // to resolve systemIds.
            try {
                factory.setFeature(
                    "http://apache.org/xml/features/validation/schema",
                    true);
            } catch (Exception ignored) {}

            parser = factory.newSAXParser().getXMLReader();
            parser.setEntityResolver(Resolve.createEntityResolver());
        } catch (Exception e) {
            throw new RuntimeException(Msg.msg("cannotCreateSAXParser", 
                                               ThrowableUtil.reason(e)));
        }

        return parser;
    }

    // -----------------------------------------------------------------------

    public static void main(String[] args) throws Exception {
        if (args.length < 2 || args.length > 3) {
            System.err.println(
                "usage: java com.xmlmind.ditac.util.LoadDocument" +
                " [-validate] in_xml_file out_xml_file");
            System.exit(1);
        }

        int i = 0;

        boolean validate = false;
        if ("-validate".equals(args[i])) {
            validate = true;
            ++i;
        }

        File inFile = new File(args[i++]);
        File outFile = new File(args[i++]);

        Document doc = LoadDocument.load(inFile, validate, null);
        SaveDocument.save(doc, outFile);
    }
}
