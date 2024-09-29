from eventum_asgi.events import Event, EventValidationException

def test_event_model():
    event = Event(event='test', data='test')
    assert event.event == 'test'
    assert event.data == 'test'
    assert event.to_json() == '{"event":"test","data":"test"}'

def test_event_model_with_invalid_data():
    event = EventValidationException(event='test', message='test')
    assert event.event == 'test'
    assert event.message == 'test'
    assert event.to_json() == '{"event":"test","message":"test"}'

if __name__ == "__main__":
    test_event_model()
