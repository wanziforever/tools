#coding=utf8
from xml.dom import minidom

def get_tag_text(element, tag):
    nodes = element.getElementsByTagName(tag)
    if len(nodes) == 0:
        return ""
    else:
        node = nodes[0]
    rc = ""
    for node in node.childNodes:
        if node.nodeType in ( node.TEXT_NODE, node.CDATA_SECTION_NODE):
            rc = rc + node.data
    return rc

class ErrorXml:
    def __init__(self, xml_string):
        self.xml = minidom.parseString(xml_string)
        self.code = get_tag_text(self.xml, 'Code')
        self.msg = get_tag_text(self.xml, 'Message')
        self.resource = get_tag_text(self.xml, 'Resource')
        self.request_id = get_tag_text(self.xml, 'RequestId')
        self.host_id = get_tag_text(self.xml, 'HostId')
    
    def show(self):
        print "Code: %s\nMessage: %s\nResource: %s\nRequestId: %s \nHostId: %s" % (self.code, self.msg, self.resource, self.request_id, self.host_id)

class Owner:
    def __init__(self, xml_element):
        self.element = xml_element
        self.id = get_tag_text(self.element, "ID")
        self.display_name = get_tag_text(self.element, "DisplayName")
    
    def show(self):
        print "ID: %s\nDisplayName: %s" % (self.id, self.display_name)

class Bucket:
    def __init__(self, xml_element):
        self.element = xml_element
        self.name = get_tag_text(self.element, "Name")
        self.creation_date = get_tag_text(self.element, "CreationDate")
    
    def show(self):
        print "Name: %s\nCreationDate: %s" % (self.name, self.creation_date)

class GetServiceXml:
    def __init__(self, xml_string):
        self.xml = minidom.parseString(xml_string)
        self.owner = Owner(self.xml.getElementsByTagName('Owner')[0])
        self.buckets = self.xml.getElementsByTagName('Bucket')
        self.bucket_list = []
        for b in self.buckets:
            self.bucket_list.append(Bucket(b))

    def show(self):
        print "Owner:"
        self.owner.show()
        print "\nBucket list:"
        for b in self.bucket_list:
            b.show()
            print ""

    def list(self):
        bl = []
        for b in self.bucket_list:
            bl.append((b.name, b.creation_date))
        return bl
    
class Content:
    def __init__(self, xml_element):
        self.element = xml_element
        self.key = get_tag_text(self.element, "Key")        
        self.last_modified = get_tag_text(self.element, "LastModified")        
        self.etag = get_tag_text(self.element, "ETag")        
        self.size = get_tag_text(self.element, "Size")        
        self.owner = Owner(self.element.getElementsByTagName('Owner')[0])
        self.storage_class = get_tag_text(self.element, "StorageClass")        

    def show(self):
        print "Key: %s\nLastModified: %s\nETag: %s\nSize: %s\nStorageClass: %s" % (self.key, self.last_modified, self.etag, self.size, self.storage_class)
        self.owner.show()

class Part:
    def __init__(self, xml_element):
        self.element = xml_element
        self.part_num = get_tag_text(self.element, "PartNumber")        
        self.object_name = get_tag_text(self.element, "PartName")
        self.object_size = get_tag_text(self.element, "PartSize")
        self.etag = get_tag_text(self.element, "ETag")

    def show(self):
        print "PartNumber: %s\nPartName: %s\nPartSize: %s\nETag: %s\n" % (self.part_num, self.object_name, self.object_size, self.etag)

class PostObjectGroupXml:
    def __init__(self, xml_string):
        self.xml = minidom.parseString(xml_string)
        self.bucket = get_tag_text(self.xml, 'Bucket')
        self.key = get_tag_text(self.xml, 'Key')
        self.size = get_tag_text(self.xml, 'Size')
        self.etag = get_tag_text(self.xml, "ETag")

    def show(self):
        print "Post Object Group, Bucket: %s\nKey: %s\nSize: %s\nETag: %s" % (self.bucket, self.key, self.size, self.etag)

class GetObjectGroupIndexXml:
    def __init__(self, xml_string):
        self.xml = minidom.parseString(xml_string)
        self.bucket = get_tag_text(self.xml, 'Bucket')
        self.key = get_tag_text(self.xml, 'Key')
        self.etag = get_tag_text(self.xml, 'Etag')
        self.file_length = get_tag_text(self.xml, 'FileLength')
        self.index_list = []
        index_lists = self.xml.getElementsByTagName('Part')
        for i in index_lists:
            self.index_list.append(Part(i))

    def list(self):
        index_list = []
        for i in self.index_list:
            index_list.append((i.part_num, i.object_name, i.object_size, i.etag))
        return index_list

    def show(self):
        print "Bucket: %s\nObject: %s\nEtag: %s\nObjectSize: %s" % (self.bucket, self.key, self.etag, self.file_length)
        print "\nPart list:"
        for p in self.index_list:
            p.show()

class GetBucketXml:
    def __init__(self, xml_string):
        self.xml = minidom.parseString(xml_string)
        self.name = get_tag_text(self.xml, 'Name')
        self.prefix = get_tag_text(self.xml, 'Prefix')
        self.marker = get_tag_text(self.xml, 'Marker')
        self.nextmarker = get_tag_text(self.xml, 'NextMarker')
        self.maxkeys = get_tag_text(self.xml, 'MaxKeys')
        self.delimiter = get_tag_text(self.xml, 'Delimiter')
        self.is_truncated = get_tag_text(self.xml, 'IsTruncated')

        self.prefix_list = []
        prefixes = self.xml.getElementsByTagName('CommonPrefixes')
        for p in prefixes:
            tag_txt = get_tag_text(p, "Prefix")
            self.prefix_list.append(tag_txt)

        self.content_list = []
        contents = self.xml.getElementsByTagName('Contents')
        for c in contents:
            self.content_list.append(Content(c))

    def show(self):
        print "Name: %s\nPrefix: %s\nMarker: %s\nNextMarker: %s\nMaxKeys: %s\nDelimiter: %s\nIsTruncated: %s" % (self.name, self.prefix, self.marker, self.nextmarker, self.maxkeys, self.delimiter, self.is_truncated)
        print "\nPrefix list:"
        for p in self.prefix_list:
            print p
        print "\nContent list:"
        for c in self.content_list:
            c.show()
            print ""

    def list(self):
        cl = []
        pl = []
        for c in self.content_list:
            cl.append((c.key, c.last_modified, c.etag, c.size, c.owner.id, c.owner.display_name, c.storage_class))
        for p in self.prefix_list:
            pl.append(p)

        return (cl, pl)
 
class GetBucketAclXml:
    def __init__(self, xml_string):
        self.xml = minidom.parseString(xml_string)
        if len(self.xml.getElementsByTagName('Owner')) != 0:
            self.owner = Owner(self.xml.getElementsByTagName('Owner')[0])
        else:
            self.owner = "" 
        self.grant = get_tag_text(self.xml, 'Grant')

    def show(self):
        print "Owner Name: %s\nOwner ID: %s\nGrant: %s" % (self.owner.id, self.owner.display_name, self.grant)
       
def test_get_bucket_xml():
    body = "<?xml version=\"1.0\" encoding=\"UTF-8\"?><ListBucketResult xmlns=\"http://s3.amazonaws.com/doc/2006-03-01/\"><Name>sweet-memory</Name><Prefix>IMG</Prefix><Marker>IMG_0</Marker><MaxKeys>1000</MaxKeys><IsTruncated>false</IsTruncated><Contents><Key>IMG_2744.JPG</Key><LastModified>2011-03-04T06:20:37.000Z</LastModified><ETag>&quot;a56047f218618a43a9b1c2dca2d8c592&quot;</ETag><Size>220778</Size><Owner><ID>2cfd76976de6f4c6f4e05fcd02680c4ca619428123681589efcb203f29dce924</ID><DisplayName>sanbo_ustc</DisplayName></Owner><StorageClass>STANDARD</StorageClass></Contents><Contents><Key>IMG_2745.JPG</Key><LastModified>2011-03-04T06:20:39.000Z</LastModified><ETag>&quot;511c0b52911bcd667338103c385741af&quot;</ETag><Size>244612</Size><Owner><ID>2cfd76976de6f4c6f4e05fcd02680c4ca619428123681589efcb203f29dce924</ID><DisplayName>sanbo_ustc</DisplayName></Owner><StorageClass>STANDARD</StorageClass></Contents><Contents><Key>IMG_3344.JPG</Key><LastModified>2011-03-04T06:20:48.000Z</LastModified><ETag>&quot;4ea11d796ecc742b216864dcf5dfd193&quot;</ETag><Size>229211</Size><Owner><ID>2cfd76976de6f4c6f4e05fcd02680c4ca619428123681589efcb203f29dce924</ID><DisplayName>sanbo_ustc</DisplayName></Owner><StorageClass>STANDARD</StorageClass></Contents><Contents><Key>IMG_3387.JPG</Key><LastModified>2011-03-04T06:20:53.000Z</LastModified><ETag>&quot;c32b5568ae4fb0a3421f0daba25ecfd4&quot;</ETag><Size>460062</Size><Owner><ID>2cfd76976de6f4c6f4e05fcd02680c4ca619428123681589efcb203f29dce924</ID><DisplayName>sanbo_ustc</DisplayName></Owner><StorageClass>STANDARD</StorageClass></Contents><Contents><Key>IMG_3420.JPG</Key><LastModified>2011-03-04T06:20:25.000Z</LastModified><ETag>&quot;edf010d2a8a4877ce0362b245fcc963b&quot;</ETag><Size>174973</Size><Owner><ID>2cfd76976de6f4c6f4e05fcd02680c4ca619428123681589efcb203f29dce924</ID><DisplayName>sanbo_ustc</DisplayName></Owner><StorageClass>STANDARD</StorageClass></Contents><Contents><Key>中文.case</Key><LastModified>2011-03-04T06:20:26.000Z</LastModified><ETag>&quot;7fd64eec21799ef048ed827cf6098f06&quot;</ETag><Size>208134</Size><Owner><ID>2cfd76976de6f4c6f4e05fcd02680c4ca619428123681589efcb203f29dce924</ID><DisplayName>sanbo_ustc</DisplayName></Owner><StorageClass>STANDARD</StorageClass></Contents></ListBucketResult>"
    h = GetBucketXml(body)
    h.show()
    (fl, pl) = h.list()
    print "\nfile_list: ", fl
    print "prefix list: ", pl

def test_get_service_xml():
    body = "<?xml version=\"1.0\" encoding=\"UTF-8\"?><ListAllMyBucketsResult xmlns=\"http://s3.amazonaws.com/doc/2006-03-01/\"><Owner><ID>2cfd76976de6f4c6f4e05fcd02680c4ca619428123681589efcb203f29dce924</ID><DisplayName>sanbo_ustc</DisplayName></Owner><Buckets><Bucket><Name>360buy</Name><CreationDate>2011-03-04T09:25:37.000Z</CreationDate></Bucket><Bucket><Name>aliyun-test-test</Name><CreationDate>2011-04-11T12:24:06.000Z</CreationDate></Bucket><Bucket><Name>irecoffee</Name><CreationDate>2011-03-04T06:14:56.000Z</CreationDate></Bucket><Bucket><Name>sweet-memory</Name><CreationDate>2011-04-12T11:56:04.000Z</CreationDate></Bucket></Buckets></ListAllMyBucketsResult>"
    h = GetServiceXml(body)
    h.show()
    print "\nbucket list: ", h.list()

def test_get_bucket_acl_xml():
    body = '<?xml version="1.0" ?><AccessControlPolicy><Owner><ID>61155b1e39dbca1d0d0f3c7faa32d9e8e9a90a9cd86edbd27d8eed5d0ad8ce82</ID><DisplayName>megjian</DisplayName></Owner><AccessControlList><Grant>public-read-write</Grant></AccessControlList></AccessControlPolicy>'
    h = GetBucketAclXml(body)
    h.show()

def test_get_object_group_xml():
    body = '<?xml version="1.0" encoding="UTF-8"?><FileGroup><Bucket>ut_test_post_object_group</Bucket> <Key>ut_test_post_object_group</Key> <Etag>&quot;91E8503F4DA1324E28434AA6B6E20D15&quot;</Etag><FileLength>1073741824</FileLength> <FilePart><Part> <PartNumber>1</PartNumber> <ObjectName>4d37380c7149508bedf78dc7c5c68f55_test_post_object_group.txt_1</ObjectName><ObjectSize>10485760</ObjectSize><ETag>&quot;A957A9F1EF44ED7D40CD5C738D113509&quot;</ETag></Part><Part><PartNumber>2</PartNumber><ObjectName>7aa26b8da263589e875d179b87642691_test_post_object_group.txt_2</ObjectName><ObjectSize>10485760</ObjectSize><ETag>&quot;A957A9F1EF44ED7D40CD5C738D113509&quot;</ETag></Part><Part><PartNumber>3</PartNumber><ObjectName>28b0c8a9bd69469f76cd102d6e1b0f03_test_post_object_group.txt_3</ObjectName><ObjectSize>10485760</ObjectSize><ETag>&quot;A957A9F1EF44ED7D40CD5C738D113509&quot;</ETag></Part></FilePart></FileGroup>'
    h = GetObjectGroupIndexXml(body)
    h.show()

if __name__ == "__main__":
    test_get_bucket_xml()
    test_get_service_xml()
    test_get_bucket_acl_xml()
    test_get_object_group_xml()

