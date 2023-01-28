from rest_framework import status
from rest_framework.test import APITestCase
from levelupapi.models import Event, Gamer, EventGamer
from levelupapi.views.event import EventSerializer

class EventTests(APITestCase):
    
    fixtures = ['gamers', 'game_types', 'games', 'events']
    
    def setUp(self):
        
        self.gamer = Gamer.objects.first()
        uid = Gamer.objects.get(uid=self.gamer.uid)
        self.client.credentials(HTTP_AUTHORIZATION=f"{uid.uid}")
        
    def test_create_event(self):
        """Create event test"""
        url = "/events"
        
        event = {
            "game": 1,
            "description": "A PlayThrough of Game About Nothing",
            "date": "2022-01-26",
            "time": "07:30:00",
            "organizer_id": 1
        }
        
        response = self.client.post(url, event, format='json')
        
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        
        new_event = Event.objects.last()
        
        expected = EventSerializer(new_event)
        
        self.assertEqual(expected.data, response.data)
    
    def test_get_event(self):
        """Get Event Test"""
        event = Event.objects.first()

        url = f'/events/{event.id}'
        
        response = self.client.get(url)
        
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        
        expected = EventSerializer(event)
        
        self.assertEqual(expected.data, response.data)
        
    def test_list_events(self):
        """Test List of Events"""
        
        url = '/events'
        
        response = self.client.get(url)
        
        all_events = Event.objects.all()
        for event in all_events:
            event.joined = len(EventGamer.objects.filter(
                gamer=self.gamer, event=event)) > 0
        expected = EventSerializer(all_events, many=True)
        
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(expected.data, response.data)
        
    def test_change_event(self):
        """test update event"""
        
        event = Event.objects.first()

        url = f'/events/{event.id}'
        
        updated_event = {
            "game": event.game.id,
            "description": f'{event. description} updated',
            "date": event.date,
            "time": event.time,
            "organizer": event.organizer.id
        }
        
        response = self.client.put(url, updated_event, format='json')
        
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        
        event.refresh_from_db()
        
        self.assertEqual(updated_event['description'], event.description)
        
    def test_delete_event(self):
        """test delete event"""
        
        event = Event.objects.first()
        
        url = f'/events/{event.id}'
        response = self.client.delete(url)
        
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        
        response = self.client.get(url)
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)
        
