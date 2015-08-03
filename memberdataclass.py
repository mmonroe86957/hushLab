import json





class Client(object):
	def __init__(self, client_data):
		self.client_data = client_data

	def get_client_names(self):
		client_names = [self.client_data[client][0] for client in range(len(self.client_data))]
		client_dict = {"clients": client_names}
		return client_dict


	def get_client_meta(self):
		client_meta_list = []
		for client in range(len(self.client_data)):
			client_name_list = [self.client_data[client][0] for client in range(len(self.client_data))]
			client_address_list = [self.client_data[client][1] for client in range(len(self.client_data))]
			client_phone_list = [self.client_data[client][2] for client in range(len(self.client_data))]
			client_email_list = [self.client_data[client][3] for client in range(len(self.client_data))]
			client_image_list = [self.client_data[client][4] for client in range(len(self.client_data))]
			

			for name, address, phone, email, image in zip(client_name_list, client_address_list, client_phone_list, client_email_list, client_image_list):
				meta_string = {"metadata": {"client": name, "address": address, "phone": phone, "email": email, "image": image}}
				#meta_obj = json.dumps(meta_string)
				client_meta_list.append(meta_string)
			return client_meta_list





class Member(object):
	def __init__(self, member_data):
		self.member_data = member_data

	def get_member_client_meta(self):
		client_data = Client(self.member_data)
		client_metadata = client_data.get_client_meta()
		return client_metadata
