from mondantic.formatting import clean_class_name, clean_field_name

def test_class_name():
    assert clean_class_name("board name") == "BoardName"
    assert clean_class_name("board#name") == "BoardName"
    assert clean_class_name("354;8wlfdrstdno") == "Wlfdrstdno"
    assert clean_class_name("board-name") == "BoardName"
    assert clean_class_name("board3453name") == "BoardName"

def test_field_name():
    assert clean_field_name("field name") == "field_name"
    assert clean_field_name("field#name") == "field_name"
    assert clean_field_name("354;8wlfdrstdno") == "wlfdrstdno"
    assert clean_field_name("field-name") == "field_name"
    assert clean_field_name("field3453name") == "field_name"
