
import keras
from keras.models import Sequential, Model
from keras.layers import *

# Rainbow sprinkles for your activation function
# @argument m: (?,N) tensor
# @returns (?,N*5) tensor
def PolyActivation(m):
	# wildcard of the day - let's do inception style activation because I've no idea which is best
	# and frequently I get great boosts from switching activation functions
	activations = ['tanh', 'sigmoid', 'softmax', 'softplus', 'relu']
	return Concatenate()([
		Activation(i)(m) for i in activations
	])


# Choose activation function for me
# More efficient than PolyActivation
# @returns Same sized tensor as input
def PolySwitchActivation(m):
	# will fail for shared nodes
	print(m.shape)

	if len(m.shape) != 3:
		# TODO: make this work in a sane way
		m = Reshape([i for i in m.shape.dims if i is not None] + [1])(m) # warning: assumes tensorflow

	activations = ['tanh', 'sigmoid', 'softmax', 'softplus', 'relu']
	return add([
		Conv1D(1,1)(Activation(i)(m)) for i in activations
	])

class Model(object):

	@classmethod
	def generate(cls, params, dataset):

		# TODO: Move this into Experiment header
		n_styles = 6
		n_sequence = 100

		if params.experiment == "review_from_visible_style":
			model = Sequential([
				Dense(8, 
					input_shape=dataset.input_shape,
					activation='softmax'),
				Dense(1, activation='sigmoid'),
			])


		elif params.experiment == "review_from_hidden_style_neighbor_conv":
			neighbors = Input(shape=(n_sequence,n_styles+2,), dtype='float32', name='neighbors')
			person = Input(shape=(n_styles,), dtype='float32', name='person')

			m = cls.style_from_neighbors(neighbors, n_styles, n_sequence)
			m = Concatenate()([m, person])
			m = Dense(n_styles*4)(m)
			m = PolyActivation(m)
			m = Dense(1, activation='sigmoid')(m)

			model = keras.models.Model(inputs=[person, neighbors], outputs=[m])

		
		elif params.experiment == "style_from_neighbor_conv":
			neighbors = Input(shape=(n_sequence,n_styles+2,), dtype='float32', name='neighbors')
			m = cls.style_from_neighbors(neighbors, n_styles, n_sequence)

			model = keras.models.Model(inputs=[neighbors], outputs=[m])


		elif params.experiment == "style_from_neighbor_rnn":
			neighbors = Input(shape=(n_sequence,n_styles+2,), dtype='float32', name='neighbors')
			m = LSTM(n_styles*4)(neighbors)
			m = Dense(n_styles)(m)
			m = Activation('sigmoid', name='final_activation')(m)

			model = keras.models.Model(inputs=[neighbors], outputs=[m])

		elif params.experiment == "review_from_all_hidden":
			neighbors = Input(shape=(n_sequence,3,), dtype='float32', name='neighbors')
			m = Conv1D(10, 1, activation='tanh')(neighbors)
			m = MaxPooling1D(n_sequence)(m)
			m = Reshape([10])(m)
			m = Dense(1)(m)
			m = PolyActivation(m)

			model = keras.models.Model(inputs=[neighbors], outputs=[m])


		# Compile time!
		if experiment.header.target == float:
			model.compile(loss=keras.losses.mean_squared_error,
				optimizer=keras.optimizers.SGD(lr=0.3),
				metrics=['accuracy'])

		elif experiment.header.target == list:
			model.compile(loss='categorical_crossentropy',
				optimizer=keras.optimizers.SGD(lr=0.3),
				metrics=['accuracy'])



		return model

	@classmethod 
	def style_from_neighbors(cls, neighbors, n_styles, n_sequence):
		m = Conv1D(n_styles, 1, activation='tanh')(neighbors)
		m = MaxPooling1D(n_sequence)(m)
		m = Reshape([n_styles])(m)
		m = Dense(n_styles)(m)
		m = Activation('softmax')(m)

		return m


