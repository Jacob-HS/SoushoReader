from website import create_app
from flask import request
import json
from flask_socketio import SocketIO, emit, join_room, leave_room, rooms, send
import random
import cv2
import os
import time
import numpy as np
from PIL import Image
import torchvision.transforms.functional as transform
import torch
from torchvision import transforms
from torch import nn
app = create_app()
socketio = SocketIO(app)

device="cpu"
classList=['U+4E00', 'U+4E01', 'U+4E03', 'U+4E07', 'U+4E08', 'U+4E09', 'U+4E0A', 'U+4E0B', 'U+4E0D', 'U+4E0E', 'U+4E11', 'U+4E14', 'U+4E16', 'U+4E18', 'U+4E19', 'U+4E1E', 'U+4E26', 'U+4E2D', 'U+4E38', 'U+4E39', 'U+4E3B', 'U+4E43', 'U+4E45', 'U+4E4B', 'U+4E4D', 'U+4E4E', 'U+4E4F', 'U+4E58', 'U+4E59', 'U+4E5D', 'U+4E5E', 'U+4E5F', 'U+4E71', 'U+4E73', 'U+4E7E', 'U+4E82', 'U+4E86', 'U+4E88', 'U+4E89', 'U+4E8B', 'U+4E8C', 'U+4E8E', 'U+4E91', 'U+4E92', 'U+4E94', 'U+4E95', 'U+4E9B', 'U+4EA1', 'U+4EA4', 'U+4EA5', 'U+4EA6', 'U+4EAB', 'U+4EAC', 'U+4EAD', 'U+4EAE', 'U+4EBA', 'U+4EC1', 'U+4ECA', 'U+4ECB', 'U+4ECD', 'U+4ED5', 'U+4ED6', 'U+4ED8', 'U+4ED9', 'U+4EE3', 'U+4EE4', 'U+4EE5', 'U+4EF0', 'U+4EF2', 'U+4EFB', 'U+4F0A', 'U+4F0D', 'U+4F0F', 'U+4F10', 'U+4F11', 'U+4F1A', 'U+4F2F', 'U+4F34', 'U+4F3C', 'U+4F46', 'U+4F4D', 'U+4F4E', 'U+4F4F', 'U+4F50', 'U+4F53', 'U+4F55', 'U+4F59', 'U+4F5B', 'U+4F5C', 'U+4F69', 'U+4F73', 'U+4F75', 'U+4F7F', 'U+4F86', 'U+4F8D', 'U+4F9B', 'U+4F9D', 'U+4FA0', 'U+4FAF', 'U+4FBF', 'U+4FC2', 'U+4FC3', 'U+4FC4', 'U+4FCA', 'U+4FD7', 'U+4FDD', 'U+4FDF', 'U+4FE1', 'U+4FEE', 'U+4FEF', 'U+5009', 'U+500B', 'U+5012', 'U+5019', 'U+501A', 'U+501F', 'U+5026', 'U+502B', 'U+5047', 'U+504F', 'U+505C', 'U+5065', 'U+5074', 'U+5076', 'U+507D', 'U+5085', 'U+508D', 'U+5099', 'U+50AC', 'U+50B3', 'U+50B7', 'U+50BE', 'U+50D5', 'U+50DE', 'U+50E7', 'U+5100', 'U+5112', 'U+5118', 'U+512A', 'U+5141', 'U+5143', 'U+5144', 'U+5145', 'U+5146', 'U+5148', 'U+5149', 'U+514B', 'U+514D', 'U+5152', 'U+5165', 'U+5168', 'U+5169', 'U+516B', 'U+516C', 'U+516D', 'U+5171', 'U+5175', 'U+5176', 'U+5177', 'U+5178', 'U+517C', 'U+5185', 'U+518D', 'U+5199', 'U+51A0', 'U+51A5', 'U+51AC', 'U+51B7', 'U+51C6', 'U+51C9', 'U+51CB', 'U+51CC', 'U+51DD', 'U+51E0', 'U+51E1', 'U+51F6', 'U+51FA', 'U+5200', 'U+5206', 'U+5207', 'U+5211', 'U+5217', 'U+521D', 'U+5224', 'U+5225', 'U+5229', 'U+5230', 'U+5236', 'U+523A', 'U+523B', 'U+5247', 'U+524A', 'U+524B', 'U+524D', 'U+525B', 'U+526F', 'U+5272', 'U+5287', 'U+5289', 'U+529B', 'U+529F', 'U+52A0', 'U+52A3', 'U+52A9', 'U+52AA', 'U+52AB', 'U+52C7', 'U+52C9', 'U+52D5', 'U+52D9', 'U+52DD', 'U+52DE', 'U+52E2', 'U+52E4', 'U+52F8', 'U+52FF', 'U+5305', 'U+5316', 'U+5317', 'U+5320', 'U+5339', 'U+533B', 'U+5341', 'U+5343', 'U+5345', 'U+5347', 'U+5348', 'U+534A', 'U+5351', 'U+5352', 'U+5357', 'U+535A', 'U+535C', 'U+536F', 'U+5370', 'U+5371', 'U+5373', 'U+5374', 'U+5377', 'U+537F', 'U+539A', 'U+539F', 'U+53AD', 'U+53BB', 'U+53C2', 'U+53C3', 'U+53C8', 'U+53CA', 'U+53CB', 'U+53CC', 'U+53CD', 'U+53D4', 'U+53D6', 'U+53D7', 'U+53D9', 'U+53DB', 'U+53E2', 'U+53E3', 'U+53E4', 'U+53E5', 'U+53EA', 'U+53EB', 'U+53EC', 'U+53EF', 'U+53F0', 'U+53F2', 'U+53F3', 'U+53F6', 'U+53F7', 'U+53F8', 'U+5404', 'U+5408', 'U+5409', 'U+540A', 'U+540C', 'U+540D', 'U+540E', 'U+540F', 'U+5410', 'U+5411', 'U+541B', 'U+541F', 'U+5426', 'U+542B', 'U+5439', 'U+543E', 'U+5442', 'U+544A', 'U+5468', 'U+5473', 'U+547C', 'U+547D', 'U+548C', 'U+54B8', 'U+54C0', 'U+54C1', 'U+54C9', 'U+54E1', 'U+54E5', 'U+54ED', 'U+54F2', 'U+5507', 'U+5510', 'U+552F', 'U+5531', 'U+5546', 'U+554F', 'U+5553', 'U+557C', 'U+5584', 'U+559C', 'U+55AA', 'U+55DA', 'U+55DF', 'U+55E3', 'U+5609', 'U+5617', 'U+562F', 'U+5668', 'U+56B4', 'U+56DB', 'U+56DE', 'U+56E0', 'U+56F0', 'U+56FA', 'U+56FD', 'U+570B', 'U+570D', 'U+5713', 'U+5716', 'U+5718', 'U+571F', 'U+5728', 'U+5730', 'U+5747', 'U+5750', 'U+5761', 'U+5782', 'U+57A2', 'U+57A3', 'U+57CE', 'U+57DF', 'U+57F7', 'U+57FA', 'U+5802', 'U+5805', 'U+582A', 'U+5831', 'U+5834', 'U+5857', 'U+585E', 'U+5875', 'U+5883', 'U+5893', 'U+58A8', 'U+58C1', 'U+58EB', 'U+58EE', 'U+58EF', 'U+58F0', 'U+58F9', 'U+58FA', 'U+58FD', 'U+590F', 'U+5915', 'U+5916', 'U+5919', 'U+591A', 'U+591C', 'U+5922', 'U+5927', 'U+5929', 'U+592A', 'U+592B', 'U+592E', 'U+5931', 'U+5937', 'U+593E', 'U+5947', 'U+5948', 'U+5949', 'U+594F', 'U+5951', 'U+5954', 'U+5955', 'U+595A', 'U+5965', 'U+596A', 'U+596E', 'U+5973', 'U+5974', 'U+597D', 'U+5982', 'U+5984', 'U+5999', 'U+59A8', 'U+59B9', 'U+59BB', 'U+59BE', 'U+59CA', 'U+59CB', 'U+59D1', 'U+59D3', 'U+59D4', 'U+59DA', 'U+59DC', 'U+59FF', 'U+5A01', 'U+5A18', 'U+5A36', 'U+5A5A', 'U+5A62', 'U+5A66', 'U+5A9A', 'U+5ACC', 'U+5AE1', 'U+5B50', 'U+5B54', 'U+5B57', 'U+5B58', 'U+5B5D', 'U+5B5F', 'U+5B63', 'U+5B64', 'U+5B66', 'U+5B6B', 'U+5B70', 'U+5B78', 'U+5B85', 'U+5B87', 'U+5B88', 'U+5B89', 'U+5B8B', 'U+5B8C', 'U+5B97', 'U+5B98', 'U+5B99', 'U+5B9A', 'U+5B9B', 'U+5B9C', 'U+5B9D', 'U+5BA2', 'U+5BA3', 'U+5BA4', 'U+5BA6', 'U+5BAE', 'U+5BB0', 'U+5BB3', 'U+5BB4', 'U+5BB5', 'U+5BB6', 'U+5BB9', 'U+5BBF', 'U+5BC2', 'U+5BC4', 'U+5BC5', 'U+5BC6', 'U+5BC7', 'U+5BCC', 'U+5BD0', 'U+5BD2', 'U+5BD3', 'U+5BDF', 'U+5BE1', 'U+5BE4', 'U+5BE6', 'U+5BE7', 'U+5BE9', 'U+5BF5', 'U+5BF6', 'U+5BF8', 'U+5BFA', 'U+5BFF', 'U+5C01', 'U+5C04', 'U+5C06', 'U+5C07', 'U+5C08', 'U+5C09', 'U+5C0A', 'U+5C0B', 'U+5C0D', 'U+5C0E', 'U+5C0F', 'U+5C11', 'U+5C1A', 'U+5C24', 'U+5C31', 'U+5C3A', 'U+5C3C', 'U+5C3D', 'U+5C3E', 'U+5C40', 'U+5C45', 'U+5C48', 'U+5C4B', 'U+5C4F', 'U+5C55', 'U+5C5E', 'U+5C60', 'U+5C65', 'U+5C71', 'U+5C90', 'U+5CA1', 'U+5CA9', 'U+5CB3', 'U+5CB8', 'U+5CE8', 'U+5CF0', 'U+5CF6', 'U+5D14', 'U+5D16', 'U+5D29', 'U+5D69', 'U+5DBA', 'U+5DDD', 'U+5DDE', 'U+5DE2', 'U+5DE5', 'U+5DE6', 'U+5DE7', 'U+5DE8', 'U+5DEE', 'U+5DF1', 'U+5DF2', 'U+5DF3', 'U+5DF7', 'U+5DFE', 'U+5E02', 'U+5E03', 'U+5E06', 'U+5E0C', 'U+5E16', 'U+5E1B', 'U+5E1D', 'U+5E2B', 'U+5E2D', 'U+5E33', 'U+5E36', 'U+5E37', 'U+5E38', 'U+5E45', 'U+5E72', 'U+5E73', 'U+5E74', 'U+5E76', 'U+5E78', 'U+5E7C', 'U+5E7D', 'U+5E7E', 'U+5E7F', 'U+5E84', 'U+5E8A', 'U+5E8F', 'U+5E95', 'U+5E9A', 'U+5E9C', 'U+5EA6', 'U+5EA7', 'U+5EAD', 'U+5EB5', 'U+5EB6', 'U+5EB7', 'U+5EB8', 'U+5EC9', 'U+5ECA', 'U+5EDF', 'U+5EE2', 'U+5EE3', 'U+5EF6', 'U+5EF7', 'U+5EFA', 'U+5EFF', 'U+5F01', 'U+5F0F', 'U+5F13', 'U+5F15', 'U+5F17', 'U+5F18', 'U+5F1F', 'U+5F25', 'U+5F31', 'U+5F35', 'U+5F37', 'U+5F48', 'U+5F4C', 'U+5F53', 'U+5F62', 'U+5F66', 'U+5F69', 'U+5F71', 'U+5F79', 'U+5F7C', 'U+5F80', 'U+5F81', 'U+5F85', 'U+5F8A', 'U+5F8B', 'U+5F8C', 'U+5F90', 'U+5F91', 'U+5F92', 'U+5F97', 'U+5F98', 'U+5F9E', 'U+5FA1', 'U+5FA9', 'U+5FAE', 'U+5FC3', 'U+5FC5', 'U+5FCD', 'U+5FD7', 'U+5FD8', 'U+5FE0', 'U+5FEB', 'U+5FF5', 'U+5FFD', 'U+6012', 'U+601C', 'U+601D', 'U+6021', 'U+6025', 'U+6027', 'U+6028', 'U+602A', 'U+6043', 'U+604B', 'U+6050', 'U+6052', 'U+6059', 'U+6065', 'U+6068', 'U+6069', 'U+606D', 'U+606F', 'U+6089', 'U+6092', 'U+6094', 'U+609F', 'U+60A3', 'U+60A6', 'U+60B2', 'U+60B5', 'U+60B6', 'U+60C5', 'U+60C6', 'U+60D1', 'U+60DC', 'U+60DF', 'U+60E0', 'U+60E1', 'U+60F3', 'U+60FB', 'U+6101', 'U+6108', 'U+610F', 'U+611A', 'U+611B', 'U+611F', 'U+6127', 'U+6148', 'U+614B', 'U+614E', 'U+6155', 'U+6162', 'U+6168', 'U+616E', 'U+6170', 'U+6176', 'U+6182', 'U+6190', 'U+6191', 'U+61B6', 'U+61C7', 'U+61C9', 'U+61F7', 'U+61F8', 'U+6200', 'U+6208', 'U+620A', 'U+620C', 'U+620E', 'U+6210', 'U+6211', 'U+6212', 'U+6216', 'U+6230', 'U+6232', 'U+6234', 'U+6236', 'U+623F', 'U+6240', 'U+6247', 'U+6249', 'U+624B', 'U+624D', 'U+6258', 'U+6276', 'U+627F', 'U+628A', 'U+6291', 'U+6295', 'U+6298', 'U+62AB', 'U+62B1', 'U+62BD', 'U+62C2', 'U+62D3', 'U+62D4', 'U+62D8', 'U+62D9', 'U+62DB', 'U+62DC', 'U+62FE', 'U+6301', 'U+6307', 'U+6309', 'U+631F', 'U+632B', 'U+632F', 'U+6355', 'U+6368', 'U+636E', 'U+6388', 'U+638C', 'U+639B', 'U+63A1', 'U+63A5', 'U+63A8', 'U+63A9', 'U+63D0', 'U+63DA', 'U+63E1', 'U+63EE', 'U+63F4', 'U+640D', 'U+6414', 'U+6416', 'U+643A', 'U+6467', 'U+6469', 'U+64AB', 'U+64B0', 'U+64CD', 'U+64DA', 'U+64EC', 'U+652F', 'U+6536', 'U+6539', 'U+653E', 'U+653F', 'U+6545', 'U+6548', 'U+6551', 'U+6559', 'U+6562', 'U+6563', 'U+6566', 'U+656C', 'U+6570', 'U+6574', 'U+6578', 'U+6587', 'U+6597', 'U+659C', 'U+65A7', 'U+65AC', 'U+65AD', 'U+65AF', 'U+65B0', 'U+65B7', 'U+65B9', 'U+65BC', 'U+65BD', 'U+65C5', 'U+65CF', 'U+65D7', 'U+65E0', 'U+65E2', 'U+65E5', 'U+65E6', 'U+65E7', 'U+65E8', 'U+65E9', 'U+65EC', 'U+6606', 'U+660C', 'U+660E', 'U+660F', 'U+6613', 'U+6614', 'U+661F', 'U+6620', 'U+6625', 'U+6627', 'U+6628', 'U+662D', 'U+662F', 'U+663C', 'U+6642', 'U+664B', 'U+665D', 'U+6666', 'U+6668', 'U+666F', 'U+6674', 'U+667A', 'U+6687', 'U+6691', 'U+6696', 'U+6697', 'U+66AB', 'U+66AE', 'U+66C9', 'U+66DC', 'U+66E0', 'U+66F0', 'U+66F2', 'U+66F4', 'U+66F8', 'U+66F9', 'U+66FE', 'U+6700', 'U+6703', 'U+6708', 'U+6709', 'U+670B', 'U+670D', 'U+6714', 'U+6717', 'U+671B', 'U+671D', 'U+671F', 'U+6728', 'U+672A', 'U+672B', 'U+672C', 'U+672D', 'U+6731', 'U+673A', 'U+673D', 'U+674E', 'U+6750', 'U+6751', 'U+6756', 'U+675C', 'U+675F', 'U+6761', 'U+6765', 'U+676D', 'U+676F', 'U+6771', 'U+6773', 'U+6777', 'U+677E', 'U+6787', 'U+6795', 'U+6797', 'U+679C', 'U+679D', 'U+67AF', 'U+67D3', 'U+67D4', 'U+67F1', 'U+67F3', 'U+67F4', 'U+6816', 'U+6821', 'U+6839', 'U+683C', 'U+6842', 'U+6843', 'U+6848', 'U+6850', 'U+6851', 'U+6853', 'U+6881', 'U+6885', 'U+689D', 'U+68A7', 'U+68A8', 'U+68C4', 'U+68D8', 'U+68E0', 'U+68F2', 'U+690D', 'U+694A', 'U+6953', 'U+695A', 'U+696D', 'U+6975', 'U+697C', 'U+69AE', 'U+69CB', 'U+6A02', 'U+6A13', 'U+6A19', 'U+6A21', 'U+6A2A', 'U+6A39', 'U+6A3D', 'U+6A4B', 'U+6A5F', 'U+6B0A', 'U+6B21', 'U+6B27', 'U+6B32', 'U+6B3A', 'U+6B47', 'U+6B4C', 'U+6B61', 'U+6B62', 'U+6B63', 'U+6B64', 'U+6B66', 'U+6B78', 'U+6B7B', 'U+6B8A', 'U+6B8B', 'U+6B98', 'U+6BB5', 'U+6BBA', 'U+6BBF', 'U+6BC0', 'U+6BCD', 'U+6BD2', 'U+6BD4', 'U+6BDB', 'U+6BEB', 'U+6C0F', 'U+6C11', 'U+6C23', 'U+6C34', 'U+6C38', 'U+6C42', 'U+6C57', 'U+6C5D', 'U+6C5F', 'U+6C60', 'U+6C7A', 'U+6C88', 'U+6C92', 'U+6C96', 'U+6C99', 'U+6CA1', 'U+6CB3', 'U+6CBB', 'U+6CBC', 'U+6CC1', 'U+6CC4', 'U+6CC9', 'U+6CD5', 'U+6CE2', 'U+6CE3', 'U+6CE5', 'U+6CE8', 'U+6CEA', 'U+6CF0', 'U+6D0B', 'U+6D12', 'U+6D17', 'U+6D1B', 'U+6D1E', 'U+6D25', 'U+6D2A', 'U+6D32', 'U+6D3B', 'U+6D3E', 'U+6D41', 'U+6D45', 'U+6D66', 'U+6D6A', 'U+6D6E', 'U+6D74', 'U+6D77', 'U+6D88', 'U+6D95', 'U+6DAF', 'U+6DB2', 'U+6DBC', 'U+6DE1', 'U+6DF1', 'U+6DF3', 'U+6DF5', 'U+6DF9', 'U+6DFA', 'U+6DFB', 'U+6E05', 'U+6E1B', 'U+6E20', 'U+6E21', 'U+6E29', 'U+6E38', 'U+6E3E', 'U+6E56', 'U+6E6F', 'U+6E7F', 'U+6E90', 'U+6E9D', 'U+6EA2', 'U+6EBA', 'U+6EC4', 'U+6EC5', 'U+6EF4', 'U+6EFF', 'U+6F01', 'U+6F06', 'U+6F0F', 'U+6F14', 'U+6F22', 'U+6F2B', 'U+6F38', 'U+6F54', 'U+6F5B', 'U+6F5C', 'U+6F64', 'U+6F6E', 'U+6F84', 'U+6FA4', 'U+6FC3', 'U+6FD5', 'U+6FDF', 'U+6FEF', 'U+706B', 'U+706F', 'U+7078', 'U+707D', 'U+7089', 'U+708E', 'U+7099', 'U+70B9', 'U+70BA', 'U+70C8', 'U+70DF', 'U+70F9', 'U+7109', 'U+711A', 'U+7121', 'U+7136', 'U+7159', 'U+7167', 'U+7169', 'U+718A', 'U+719F', 'U+71B1', 'U+71C8', 'U+71D5', 'U+71DF', 'U+71E5', 'U+71ED', 'U+7210', 'U+722D', 'U+7232', 'U+7235', 'U+7236', 'U+723D', 'U+723E', 'U+7246', 'U+7247', 'U+7252', 'U+7259', 'U+725B', 'U+7267', 'U+7269', 'U+7279', 'U+727D', 'U+72A2', 'U+72AF', 'U+72B6', 'U+72C2', 'U+72D0', 'U+72EC', 'U+72FC', 'U+732E', 'U+7336', 'U+733F', 'U+7368', 'U+7372', 'U+7378', 'U+737B', 'U+7384', 'U+7387', 'U+7389', 'U+738B', 'U+73CD', 'U+73E0', 'U+73FE', 'U+7406', 'U+7434', 'U+745E', 'U+74A7', 'U+74B0', 'U+74CA', 'U+74E6', 'U+7518', 'U+751A', 'U+751F', 'U+7528', 'U+752B', 'U+7530', 'U+7531', 'U+7532', 'U+7533', 'U+7537', 'U+753B', 'U+754C', 'U+7554', 'U+7559', 'U+755D', 'U+7562', 'U+7565', 'U+756B', 'U+7570', 'U+7576', 'U+7591', 'U+75B2', 'U+75BE', 'U+75C5', 'U+75DB', 'U+75F4', 'U+7678', 'U+767B', 'U+767C', 'U+767D', 'U+767E', 'U+7684', 'U+7686', 'U+7687', 'U+76AE', 'U+76CA', 'U+76D6', 'U+76D7', 'U+76DB', 'U+76DC', 'U+76DF', 'U+76E1', 'U+76E4', 'U+76EE', 'U+76F4', 'U+76F8', 'U+7701', 'U+7709', 'U+770B', 'U+771F', 'U+7720', 'U+7737', 'U+773A', 'U+773C', 'U+7740', 'U+7761', 'U+7763', 'U+7766', 'U+77BB', 'U+77DB', 'U+77E2', 'U+77E3', 'U+77E5', 'U+77E9', 'U+77ED', 'U+77F3', 'U+7814', 'U+7834', 'U+788E', 'U+7891', 'U+78A7', 'U+78D0', 'U+78E8', 'U+793A', 'U+793C', 'U+793E', 'U+7948', 'U+7956', 'U+7957', 'U+795D', 'U+795E', 'U+7960', 'U+7965', 'U+796D', 'U+797F', 'U+7981', 'U+7984', 'U+7985', 'U+798D', 'U+798F', 'U+79A6', 'U+79AA', 'U+79AE', 'U+79BD', 'U+79C0', 'U+79C1', 'U+79CB', 'U+79D1', 'U+79D8', 'U+79E6', 'U+79F0', 'U+79FB', 'U+7A00', 'U+7A0B', 'U+7A0D', 'U+7A1A', 'U+7A2E', 'U+7A31', 'U+7A37', 'U+7A3B', 'U+7A3C', 'U+7A3D', 'U+7A3F', 'U+7A40', 'U+7A4D', 'U+7A76', 'U+7A7A', 'U+7A7F', 'U+7A81', 'U+7A97', 'U+7AAE', 'U+7ACA', 'U+7ACB', 'U+7ADF', 'U+7AE0', 'U+7AE5', 'U+7AEF', 'U+7AF6', 'U+7AF9', 'U+7B0B', 'U+7B11', 'U+7B19', 'U+7B2C', 'U+7B46', 'U+7B49', 'U+7B4D', 'U+7B51', 'U+7B54', 'U+7B56', 'U+7B75', 'U+7B95', 'U+7B97', 'U+7BA1', 'U+7BB1', 'U+7BC0', 'U+7BC4', 'U+7BC6', 'U+7BC7', 'U+7BC9', 'U+7BE4', 'U+7C21', 'U+7C3E', 'U+7C4D', 'U+7C60', 'U+7C6C', 'U+7C73', 'U+7C89', 'U+7C97', 'U+7C9F', 'U+7CAE', 'U+7CBE', 'U+7CDF', 'U+7CE0', 'U+7CE7', 'U+7CFB', 'U+7D00', 'U+7D04', 'U+7D05', 'U+7D0D', 'U+7D19', 'U+7D1B', 'U+7D20', 'U+7D21', 'U+7D22', 'U+7D2B', 'U+7D2F', 'U+7D30', 'U+7D39', 'U+7D42', 'U+7D44', 'U+7D50', 'U+7D66', 'U+7D72', 'U+7D76', 'U+7D93', 'U+7DAD', 'U+7DB1', 'U+7DBA', 'U+7DBF', 'U+7DD1', 'U+7DE8', 'U+7DE9', 'U+7DFB', 'U+7E23', 'U+7E37', 'U+7E3B', 'U+7E3D', 'U+7E3E', 'U+7E41', 'U+7E5E', 'U+7E69', 'U+7E7C', 'U+7E8C', 'U+7E8F', 'U+7F3A', 'U+7F54', 'U+7F6A', 'U+7F6E', 'U+7F77', 'U+7F85', 'U+7F88', 'U+7F8A', 'U+7F8E', 'U+7F94', 'U+7F9E', 'U+7FA4', 'U+7FA9', 'U+7FBD', 'U+7FC1', 'U+7FD2', 'U+7FD4', 'U+7FE0', 'U+7FF0', 'U+7FFC', 'U+8001', 'U+8003', 'U+8005', 'U+800C', 'U+8033', 'U+803B', 'U+803D', 'U+804A', 'U+8056', 'U+805A', 'U+805E', 'U+8072', 'U+8077', 'U+8086', 'U+8089', 'U+808C', 'U+80A5', 'U+80A9', 'U+80AF', 'U+80B2', 'U+80CC', 'U+80E1', 'U+80F8', 'U+80FD', 'U+811A', 'U+8131', 'U+8155', 'U+816B', 'U+8170', 'U+8178', 'U+8179', 'U+819D', 'U+81B3', 'U+81C2', 'U+81D8', 'U+81E3', 'U+81E8', 'U+81EA', 'U+81F3', 'U+81F4', 'U+81FA', 'U+8205', 'U+8207', 'U+8208', 'U+820A', 'U+820C', 'U+820D', 'U+821C', 'U+821E', 'U+821F', 'U+822C', 'U+8239', 'U+826F', 'U+8271', 'U+8272', 'U+8292', 'U+8299', 'U+829D', 'U+82A5', 'U+82B1', 'U+82B3', 'U+82D1', 'U+82D4', 'U+82DF', 'U+82E5', 'U+82E6', 'U+82F1', 'U+8302', 'U+8303', 'U+8305', 'U+8336', 'U+8338', 'U+8349', 'U+834A', 'U+8352', 'U+8377', 'U+838A', 'U+83AB', 'U+83B1', 'U+83CA', 'U+83DC', 'U+83EF', 'U+842C', 'U+843D', 'U+8449', 'U+8457', 'U+845B', 'U+8463', 'U+8499', 'U+84B2', 'U+84B8', 'U+84BC', 'U+84C9', 'U+84CB', 'U+84EC', 'U+84EE', 'U+8521', 'U+8569', 'U+8584', 'U+8591', 'U+85AA', 'U+85CD', 'U+85CF', 'U+85DD', 'U+85E4', 'U+85E5', 'U+8607', 'U+862D', 'U+864E', 'U+8655', 'U+865A', 'U+865E', 'U+865F', 'U+866B', 'U+8679', 'U+86C7', 'U+86DF', 'U+8700', 'U+871C', 'U+878D', 'U+87F2', 'U+8846', 'U+884C', 'U+8853', 'U+885B', 'U+885D', 'U+8863', 'U+8868', 'U+8870', 'U+8881', 'U+888D', 'U+8896', 'U+88AB', 'U+88C1', 'U+88C5', 'U+88CF', 'U+88D8', 'U+88DC', 'U+88DD', 'U+88E1', 'U+88F3', 'U+88F9', 'U+88FD', 'U+8944', 'U+895F', 'U+897F', 'U+8981', 'U+8986', 'U+898B', 'U+898F', 'U+8996', 'U+89AA', 'U+89BA', 'U+89C0', 'U+89D2', 'U+89E3', 'U+89E6', 'U+89F8', 'U+8A00', 'U+8A08', 'U+8A13', 'U+8A18', 'U+8A2A', 'U+8A2D', 'U+8A31', 'U+8A3B', 'U+8A55', 'U+8A5E', 'U+8A60', 'U+8A63', 'U+8A66', 'U+8A69', 'U+8A71', 'U+8A73', 'U+8A85', 'U+8A89', 'U+8A8C', 'U+8A93', 'U+8A9E', 'U+8AA0', 'U+8AA4', 'U+8AAC', 'U+8AB0', 'U+8ABF', 'U+8AC7', 'U+8ACB', 'U+8AD6', 'U+8AF8', 'U+8B00', 'U+8B02', 'U+8B19', 'U+8B1B', 'U+8B1D', 'U+8B49', 'U+8B4F', 'U+8B58', 'U+8B6C', 'U+8B70', 'U+8B77', 'U+8B7D', 'U+8B80', 'U+8B8A', 'U+8B93', 'U+8C37', 'U+8C46', 'U+8C48', 'U+8C50', 'U+8C61', 'U+8C8C', 'U+8C9E', 'U+8CA0', 'U+8CA1', 'U+8CA2', 'U+8CA7', 'U+8CAA', 'U+8CAC', 'U+8CB4', 'U+8CB7', 'U+8CBB', 'U+8CC0', 'U+8CC7', 'U+8CCA', 'U+8CD3', 'U+8CDC', 'U+8CDE', 'U+8CE2', 'U+8CE4', 'U+8CE6', 'U+8CEA', 'U+8D08', 'U+8D64', 'U+8D70', 'U+8D74', 'U+8D77', 'U+8D85', 'U+8D8A', 'U+8D99', 'U+8DA3', 'U+8DB3', 'U+8DE1', 'U+8DEF', 'U+8E2A', 'U+8E64', 'U+8E8D', 'U+8EAB', 'U+8EAC', 'U+8ECA', 'U+8ECD', 'U+8ED2', 'U+8F09', 'U+8F14', 'U+8F15', 'U+8F1D', 'U+8F29', 'U+8F2A', 'U+8F3F', 'U+8F49', 'U+8F9B', 'U+8F9E', 'U+8F9F', 'U+8FA8', 'U+8FB0', 'U+8FB1', 'U+8FB2', 'U+8FCE', 'U+8FD1', 'U+8FD4', 'U+8FE9', 'U+8FEB', 'U+8FF0', 'U+8FF7', 'U+8FF9', 'U+8FFD', 'U+9000', 'U+9001', 'U+9006', 'U+900D', 'U+9010', 'U+9014', 'U+901A', 'U+901D', 'U+901F', 'U+9020', 'U+9022', 'U+9023', 'U+9032', 'U+9038', 'U+903C', 'U+9042', 'U+9047', 'U+904A', 'U+904B', 'U+904D', 'U+904E', 'U+9053', 'U+9054', 'U+9055', 'U+9059', 'U+9060', 'U+9063', 'U+9065', 'U+9069', 'U+9072', 'U+907A', 'U+907D', 'U+907F', 'U+9084', 'U+908A', 'U+9091', 'U+90A3', 'U+90AA', 'U+90AF', 'U+90C1', 'U+90CA', 'U+90CE', 'U+90E1', 'U+90E8', 'U+90ED', 'U+90FD', 'U+9119', 'U+9149', 'U+914C', 'U+9152', 'U+916C', 'U+9178', 'U+9189', 'U+9192', 'U+919C', 'U+91AB', 'U+91C7', 'U+91CB', 'U+91CC', 'U+91CD', 'U+91CE', 'U+91CF', 'U+91D1', 'U+91E3', 'U+920E', 'U+9264', 'U+9280', 'U+9285', 'U+9298', 'U+9304', 'U+9322', 'U+9326', 'U+932B', 'U+9332', 'U+937E', 'U+93AE', 'U+93E1', 'U+9418', 'U+9435', 'U+9577', 'U+9580', 'U+958B', 'U+958F', 'U+9591', 'U+9593', 'U+95A3', 'U+95CC', 'U+95D5', 'U+95DC', 'U+9632', 'U+963F', 'U+9644', 'U+964B', 'U+964D', 'U+9650', 'U+9662', 'U+9664', 'U+966A', 'U+9670', 'U+9673', 'U+9675', 'U+9676', 'U+9678', 'U+967D', 'U+9685', 'U+9686', 'U+968E', 'U+968F', 'U+9694', 'U+969B', 'U+96A8', 'U+96B1', 'U+96BB', 'U+96C0', 'U+96C1', 'U+96C4', 'U+96C5', 'U+96C6', 'U+96D5', 'U+96D6', 'U+96D9', 'U+96DC', 'U+96DE', 'U+96E2', 'U+96E3', 'U+96E8', 'U+96EA', 'U+96F2', 'U+96F6', 'U+96F7', 'U+9707', 'U+971C', 'U+971E', 'U+9727', 'U+9732', 'U+9748', 'U+9752', 'U+9756', 'U+9759', 'U+975C', 'U+975E', 'U+9761', 'U+9762', 'U+9769', 'U+978D', 'U+97A0', 'U+97F3', 'U+97FB', 'U+97FF', 'U+9803', 'U+9806', 'U+9808', 'U+980C', 'U+9813', 'U+9817', 'U+9818', 'U+982D', 'U+983B', 'U+984C', 'U+984F', 'U+9854', 'U+9858', 'U+985B', 'U+985E', 'U+9867', 'U+98A8', 'U+98DB', 'U+98DF', 'U+98E2', 'U+98EF', 'U+98F2', 'U+98FD', 'U+990A', 'U+9910', 'U+9918', 'U+9928', 'U+9951', 'U+9996', 'U+9999', 'U+99A8', 'U+99AC', 'U+99B3', 'U+99D2', 'U+99D5', 'U+99ED', 'U+9A45', 'U+9A55', 'U+9A57', 'U+9A5A', 'U+9A62', 'U+9AA8', 'U+9AB8', 'U+9AD4', 'U+9AD8', 'U+9AEE', 'U+9B1A', 'U+9B31', 'U+9B3C', 'U+9B42', 'U+9B44', 'U+9B4F', 'U+9B5A', 'U+9B6F', 'U+9BAE', 'U+9BC9', 'U+9C57', 'U+9CE5', 'U+9CF3', 'U+9CF4', 'U+9D5D', 'U+9DB4', 'U+9DC4', 'U+9DD7', 'U+9E1E', 'U+9E7D', 'U+9E7F', 'U+9E97', 'U+9E9F', 'U+9EA6', 'U+9EB5', 'U+9EC4', 'U+9ECD', 'U+9ECE', 'U+9ED8', 'U+9EDE', 'U+9F0E', 'U+9F13', 'U+9F20', 'U+9F3B', 'U+9F4A', 'U+9F4B', 'U+9F52', 'U+9F61', 'U+9F8D', 'U+9F9C']

class model1(nn.Module):
  def __init__(self, output_shape: int):
    super().__init__()
    self.block_1=nn.Sequential(
      nn.Conv2d(in_channels=1, out_channels=32, kernel_size=3, stride=1, padding=1),
      nn.ReLU(),
      nn.Conv2d(in_channels=32, out_channels=32, kernel_size=3, stride=1, padding=1),
      nn.ReLU(),
      nn.MaxPool2d(kernel_size=2, stride=2)
    )

    self.block_2=nn.Sequential(
      nn.Conv2d(in_channels=32,out_channels=64,kernel_size=3, stride=1, padding=1),
      nn.ReLU(),
      nn.Conv2d(in_channels=64,out_channels=64,kernel_size=3, stride=1, padding=1),
      nn.ReLU(),
      nn.MaxPool2d(2),
      nn.Conv2d(in_channels=64,out_channels=128,kernel_size=3, stride=1, padding=1),
      nn.ReLU(),
      nn.Conv2d(in_channels=128,out_channels=128,kernel_size=3, stride=1, padding=1),
      nn.ReLU(),
      nn.MaxPool2d(2)
    )

    self.classifier = nn.Sequential(
        nn.Flatten(),
        nn.Dropout(.5),
        nn.Linear(in_features=8192 ,out_features=1024),
        nn.Dropout(.5),
        nn.Linear(in_features=1024 ,out_features=1024),
        nn.Linear(in_features=1024 ,out_features=output_shape)
    )

  def forward(self, x: torch.Tensor):
    return self.classifier(self.block_2(self.block_1(x)))
model=model1(output_shape=len(classList)).to(device)
model.load_state_dict(torch.load("test.pth", map_location=device))
def assessCustomImage(image, numOfResponses=1):
  global model
  image1 = image
  try:
    img = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
  except:
    img=image1
  imageFinal=cv2.resize(img, (64,64))
  im_pil = Image.fromarray(imageFinal)
  customImageuint8=transform.to_tensor(im_pil)
  imageTransform=transforms.Compose([transforms.Grayscale(num_output_channels=1)])
  customImage=imageTransform(customImageuint8).to(device)
  model.eval()
  with torch.inference_mode():
    yPred=model(customImage.to(device).unsqueeze(dim=0))
    yPredClass=torch.topk(torch.softmax(yPred,dim=1),k=numOfResponses, dim=1).indices
    return [chr(int(classList[yPredClass.tolist()[0][i]][2:],16)) for i in range(numOfResponses)]

@socketio.event
def askQuestion (data):
    print("fuck yeet")
    print(os.listdir('.'))
    print(os.listdir('website'))
    #global model
    #answerList={}
    #for idx in range(len(data)):
    #  im = cv2.imdecode(np.array(data[str(idx+1)], dtype=np.uint8), cv2.IMREAD_UNCHANGED)
    #  result=assessCustomImage(im, 5)
    #  info={}
    #  for kanji in result:
    #    i='U+'+hex(ord(kanji)).upper()[2:]
    #    info[kanji]=os.listdir('website\\static\\samples\\'+i)
    #  answerList[str(idx+1)]=info
#
    #socketio.emit("answer", answerList)

if __name__ == '__main__':
    socketio.run(app, debug=True)
