---
layout: doc
origin: model
language: application
type: grammar
version: 26
---


## root


### user

	'user' ['users'] component 'modifier'

### allow anonymous user

	'allow anonymous user' stategroup (
		'no'
		'yes' [ 'anonymous' ]
	)

### has dynamic users

	'has dynamic users' stategroup (
		'no'
		'yes'
			'context node path' [ 'dynamic' ':' ] component 'node content path'
			'users dictionary' [ '.' ] reference
			'password node' ['password' ':'] component 'node content path'
			'password property' [ '.' ] reference
	)

### roles

	'roles' [ 'roles' ] collection indent (
		'condition' [ ':' ] stategroup (
			'interface' [ 'interface' ]
				'modifier' component 'modifier'
			'user'
				'dynamic' stategroup (
					'no'
					'yes' [ 'dynamic' ]
						'path' component 'node content path'
				)
				'anonymous' stategroup (
					'no'
					'yes' [ 'anonymous' ]
				)
		)
	)

### source base

	'source base' group (
		'elementary' component 'value source base'
		'derived' component 'value source base'
	)

### source

	'source' group (
		'user'			component 'value source'
		'meta'			component 'value source'
		'inference'		component 'value source'
		'calculation'	component 'value source'
	)

### integer

	'integer' component 'integer'

### natural

	'natural' component 'natural'

### type

	'type' [ 'root' ] component 'type'

### root mutation permission

	'root mutation permission' component 'mutation permission definition'

### root read permission

	'root read permission' component 'read permission definition'

### dependable

	'dependable' component 'dependency'

### entity

	'entity' component 'entity'

### root

	'root' component 'node'

### numerical types

	'numerical types' [ 'numerical-types' ] collection indent (
		'type' stategroup (
			'relative' ['in']
				'range type' reference
			'absolute'
				'product conversions' collection indent ( ['=']
					'right' ['*'] reference
				)
				'division conversions' collection indent ( ['=']
					'denominator' ['/'] reference
				)
		)
		'singular conversions' collection indent ( ['=']
			'type' stategroup (
				'factor'
					'invert' stategroup (
						'no' ['*']
						'yes' ['/']
					)
					'factor' number
					'base' ['*'] number
					'exponent' ['^'] number
				'base'
					'offset' ['+'] number
					'base' ['*'] number
					'exponent' ['^'] number
					'unit conversion' stategroup (
						'no'
							'constraint' component 'numerical type constraint'
						'yes'
							'conversion rule' ['in'] reference
					)
			)
		)
	)

## component rules


### value source base

	'value source base'

### value source

	'value source'

### value

	'value'

### elementary value

	'elementary value'
		'value' component 'value'

### derived value

	'derived value'
		'value' component 'value'

### dependency

	'dependency'

### constraints

	'constraints'
		'constraints' collection (
			'type' [':'] stategroup (
				'acyclic' [ 'acyclic-graph' ]
				'linear' [ 'ordered-graph' ]
			)
		)

### selection type

	'selection type'

### backward selection

	'backward selection'
		'tag' component 'selection type'

### forward selection

	'forward selection'
		'tag' component 'selection type'

### modifier

	'modifier'

### type

	'type'

### set type

	'set type'

### integer

	'integer'
		'set type' component 'set type'

### natural

	'natural'
		'set type' component 'set type'

### entity

	'entity'

### resolved node selection starting from property

	'resolved node selection starting from property'
		'type' stategroup (
			'input parameter'
				'type' stategroup (
					'state'
						'context selection' component 'context property selection'
						'state' stategroup (
							'state'
						)
						'input parameter' [ '&' ] reference
				)
				'tail' component 'resolved node descendant selection starting from node'
			'this node'
				'context selection' component 'context property selection'
				'type' stategroup (
					'group'
						'group' [ '+' ] reference
						'tail' component 'resolved node descendant selection starting from node'
					'state group output parameter'
						'state group' [ '?' ] reference
						'output parameter' [ '$' ] reference
					'referencer output'
						'referencer type' stategroup (
							'matrix' [ '>key' ]
								'output type' stategroup (
									'referenced node'
									'output parameter'
										'output parameter' [ '$' ] reference
								)
							'reference'
								'reference' [ '>' ] reference
								'output type' stategroup (
									'referenced node'
									'output parameter'
										'output parameter' [ '$' ] reference
								)
						)
				)
		)

### resolved state group selection starting from property

	'resolved state group selection starting from property'
		'type' stategroup (
			'state group'
				'context selection' component 'context property selection'
				'state group' [ '?' ] reference
			'node'
				'selection' component 'resolved node selection starting from property'
				'state group' [ '?' ] reference
		)

### resolved collection selection starting from property

	'resolved collection selection starting from property'
		'type' stategroup (
			'dictionary'
				'context selection' component 'context property selection'
				'dictionary' [ '.' ] reference
			'matrix'
				'context selection' component 'context property selection'
				'matrix' [ '%' ] reference
			'node'
				'selection' component 'resolved node selection starting from property'
				'collection type' stategroup (
					'dictionary'
						'dictionary' [ '.' ] reference
					'matrix'
						'matrix' [ '%' ] reference
				)
		)

### resolved node descendant selection starting from node

	'resolved node descendant selection starting from node'
		'group selection' component 'group node selection' //NOTE: not supported by parser generator
		'type' stategroup (
			'this node'
				'state group output parameter'
					'state group' [ '?' ] reference
					'output parameter' [ '$' ] reference
				'referencer output'
					'referencer type' stategroup (
						'matrix' [ '>key' ]
						'output type' stategroup (
							'referenced node'
							'output parameter'
								'output parameter' [ '$' ] reference
						)
						'reference'
							'reference' [ '>' ] reference
								'output type' stategroup (
									'referenced node'
									'output parameter'
										'output parameter' [ '$' ] reference
								)
					)
		)
	//'reference selection path'
	//	'context' stategroup (
	//		'this node'
	//			'context selection' component 'context node selection'
	//		'output parameter'
	//			'context selection' component 'context node selection'
	//			'type' stategroup (
	//				'component output'
	//					'component' [ '~' ] reference
	//					'output type' stategroup (
	//						'component node'
	//						'output parameter'
	//							'output parameter' [ '$' ] reference
	//					)
	//				'state group output parameter'
	//					'state group' [ '?' ] reference
	//					'output parameter' [ '$' ] reference
	//				'referencer output'
	//					'referencer type' stategroup (
	//						'matrix' [ '>key' ]
	//						'output type' stategroup (
	//							'referenced node'
	//							'output parameter'
	//								'output parameter' [ '$' ] reference
	//						)
	//						'reference' [ '>' ]
	//							'reference' reference
	//							'output type' stategroup (
	//								'referenced node'
	//								'output parameter'
	//									'output parameter' [ '$' ] reference
	//							)
	//					)
	//			)
	//		'input parameter'
	//			'type' stategroup (
	//				'component' [ '&' ]
	//					'input parameter' reference
	//			)
	//			'tail' component 'context node selection'
	//	)

### derivation selection path

	'derivation selection path'
		'context' stategroup (
			'this node'
				'context selection' component 'derivation node selection'
			'output parameter'
				'context selection' component 'derivation node selection'
				'type' stategroup (
					'state group output parameter'
						'state group' [ '?' ] reference
						'output parameter' [ '$' ] reference
					'referencer output'
						'referencer type' stategroup (
							'matrix' [ '>key' ]
							'output type' stategroup (
								'referenced node'
								'output parameter'
									'output parameter' [ '$' ] reference
							)
							'reference' [ '>' ]
								'reference' reference
								'output type' stategroup (
									'referenced node'
									'output parameter'
										'output parameter' [ '$' ] reference
								)
						)
				)
			'input parameter'
				'context node selection' component 'derivation node selection'
				'type' stategroup (
					'state' [ '&' ]
						'input parameter' reference
				)
				'tail' component 'derivation node selection'
		)

### node content path

	'node content path'
		'has steps' stategroup (
			'no'
			'yes'
				'type' stategroup (
					'state'
						'state group' [ '?' ] reference
						'state' [ '|' ] reference
					'group'
						'group' [ '+' ] reference
				)
				'tail' component 'node content path'
		)

### traversed derivation node content path

	'traversed derivation node content path'
		'step back' stategroup (
			'no'
			'yes'
				'type' stategroup (
					'state' [ '?^' ]
					'group' [ '+^' ]
				)
				'tail' component 'traversed derivation node content path'
		)

### group context property selection

	'group context property selection'
		'has steps' stategroup (
			'no'
			'yes' [ '+^' ]
				'tail' component 'group context property selection'
		)

### entity scoped context property selection

	'entity scoped context property selection'
		'has steps' stategroup (
			'no'
			'yes'
				'type' stategroup (
					'state parent' [ '?^' ]
					'group parent' [ '+^' ]
				)
				'tail' component 'entity scoped context property selection'
		)

### entity scoped context node selection

	'entity scoped context node selection'
		'has steps' stategroup (
			'no'
			'yes'
				'type' stategroup (
					'state parent' [ '?^' ]
					'group parent' [ '+^' ]
				)
				'tail' component 'entity scoped context node selection'
		)

### unresolved node selection

	'unresolved node selection'
		'type' stategroup (
			'this node'
				'context selection' component 'context property selection'
				'type' stategroup (
					'this'
					'referencer output'
						'referencer type' stategroup (
							'matrix' [ '>key' ]
							'reference'
								'reference' [ '>' ] reference
						)
				)
		)
		'tail' component 'group node selection'

### context node selection

	'context node selection'
		'has steps' stategroup (
			'no'
			'yes'
				'type' stategroup (
					'dictionary parent' [ '.^' ]
					'matrix parent' [ '%^' ]
					'state parent' [ '?^' ]
					'group parent' [ '+^' ]
					'group'
						'group' [ '+' ] reference
				)
				'tail' component 'context node selection'
		)

### ancestor node selection

	'ancestor node selection'
		'has steps' stategroup (
			'no'
			'yes'
				'type' stategroup (
					'dictionary parent' [ '.^' ]
					'matrix parent' [ '%^' ]
					'state parent' [ '?^' ]
					'group parent' [ '+^' ]
				)
				'tail' component 'ancestor node selection'
		)

### context property selection

	'context property selection'
		'has steps' stategroup (
			'no'
			'yes'
				'type' stategroup (
					'dictionary parent' [ '.^' ]
					'matrix parent' [ '%^' ]
					'state parent' [ '?^' ]
					'group parent' [ '+^' ]
				)
				'tail' component 'context property selection'
		)

### group node selection

	'group node selection'
		'has steps' stategroup (
			'no'
			'yes'
				'group' [ '+' ] reference
				'tail' component 'group node selection'
		)

### derivation node content path

	'derivation node content path'
		'has steps' stategroup (
			'no'
			'yes'
				'type' stategroup (
					'state'
						'state group' [ '?' ] reference
						'state' [ '|' ] reference
					'group'
						'group' [ '+' ] reference
				)
				'tail' component 'derivation node content path'
		)

### derivation node selection

	'derivation node selection'
		'has steps' stategroup (
			'no'
			'yes'
				'type' stategroup (
					'dictionary parent' [ '.^' ]
					'matrix parent' [ '%^' ]
					'state parent' [ '?^' ]
					'group parent' [ '+^' ]
					'group'
						'group' [ '+' ] reference
				)
				'tail' component 'derivation node selection'
		)

### calculated input parameter node selection

	'calculated input parameter node selection'
		'type' stategroup (
			'state'
				'context selection' component 'ancestor node selection'
				'state' stategroup ( 'state' )
				'input parameter' [ '&' ] reference
		)

### calculated descendant node selection starting from node

	'calculated descendant node selection starting from node'
		'group selection' component 'group node selection' //NOTE: not supported by parser generator
		'type' stategroup (
			'this node'
			'state group output parameter'
				'state group' [ '?' ] reference
				'output parameter' [ '$' ] reference
			'referencer output'
				'referencer type' stategroup (
					'matrix' [ '>key' ]
						// 'backward' stategroup ( 'backward' )
						'output type' stategroup (
							'referenced node'
							'output parameter'
								'output parameter' [ '$' ] reference
						)
					'reference'
						// 'backward' stategroup ( 'backward' )
						'reference' [ '>' ] reference
						'output type' stategroup (
							'referenced node'
							'output parameter'
								'output parameter' [ '$' ] reference
						)
					)
		)

### calculated descendant node selection starting from property

	'calculated descendant node selection starting from property'
		'type' stategroup (
			'group'
				'group' [ '+' ] reference
				'tail' component 'calculated descendant node selection starting from node'
			'state group output parameter'
				'state group' [ '?' ] reference
				'output parameter' [ '$' ] reference
			'referencer output'
				'referencer type' stategroup (
					'matrix' [ '>key' ]
						// 'backward' stategroup ( 'backward' )
						'output type' stategroup (
							'referenced node'
							'output parameter'
								'output parameter' [ '$' ] reference
						)
					'reference'
						'reference' [ '>' ] reference
						// 'backward' stategroup ( 'backward' )
						'output type' stategroup (
							'referenced node'
							'output parameter'
								'output parameter' [ '$' ] reference
						)
				)
		)

### calculated node selection starting from property

	'calculated node selection starting from property'
		'type' stategroup (
			'input parameter'
				'selection' component 'calculated input parameter node selection'
				'tail' component 'calculated descendant node selection starting from node'
			'this node'
				'context selection' component 'context property selection'
				'selection' component 'calculated descendant node selection starting from property'
		)

### calculated collection selection starting from property

	'calculated collection selection starting from property'
		'type' stategroup (
			'collection'
				'context selection' component 'context property selection'
				'type' stategroup (
					'dictionary' [ '.' ]
					'matrix' [ '%' ]
				)
				'collection' reference
			'node'
				'selection' component 'calculated node selection starting from property'
				'type' stategroup (
					'dictionary' [ '.' ]
					'matrix' [ '%' ]
				)
				'collection' reference
		)

### calculated state group selection starting from property

	'calculated state group selection starting from property'
		'type' stategroup (
			'state group'
				'context selection' component 'context property selection'
				'state group' [ '?' ] reference
			'node'
				'selection' component 'calculated node selection starting from property'
				'state group' [ '?' ] reference
		)

### node path

	'node path'
		'steps' component 'node path step'

### node path step

	'node path step'
		'has steps' stategroup (
			'no'
			'yes'
				'type' stategroup (
					'state'
						'state group' [ '?' ] reference
						'state' [ '|' ] reference
					'group'
						'group' [ '+' ] reference
					'dictionary'
						'dictionary' [ '.' ] reference
					'matrix'
						'matrix' [ '%' ] reference
				)
				'tail' component 'node path step'
		)

### referencer

	'referencer'
		'dependable' component 'dependency'

### mutation permission definition

	'mutation permission definition'
		'role' [ '#writer' ] reference

### read permission definition

	'read permission definition'
		'role' [ '#reader' ] reference

### state instantiation

	'state instantiation'
		'state' reference
		'input arguments' collection ( [ '(' , ')' ]
			'constraint' stategroup ( 'node type' )
			'selection' [ '=>' ] component 'calculated node selection starting from property'
		)

### state instantiation 2

	'state instantiation 2'
		'state' reference
		'input arguments' collection ( [ '(' , ')' ]
			'context' [ '=>' ] stategroup (
				'state group property'
					'selection' component 'calculated node selection starting from property'
				'expression result node' [ '$' ]
					'selection' component 'calculated descendant node selection starting from node'
			)
		)

### conditional state group expression

	'conditional state group expression'
		'has steps' stategroup (
			'no'
				'state' reference
				'input arguments' collection ( [ '(' , ')' ]
					'expression context' [ '=>' ] component 'conditional state group expression context path'
					'context selection' stategroup (
						'target context' [ '$^' ]
							'selection' component 'calculated node selection starting from property'
						'expression result' [ '$' ] //NOTE: keyword '$' is temporary
							'context type' stategroup (
								'input parameter'
									'input parameter' [ '&' ] reference
								'this state'
							)
							'selection' component 'calculated descendant node selection starting from node'
					)
				)
			'yes' ['switch' '(']
				'expression context' component 'conditional state group expression context path'
				'type' stategroup (
					'merge' [ '$^' ]
						'state group selection' component 'calculated state group selection starting from property'
					'flatten' ['$']
						'context type' stategroup (
							'input parameter'
								'input parameter' [ '&' ] reference
							'this state'
						)
						'selection' component 'calculated descendant node selection starting from node'
						'state group' [ '?' ] reference
				)
				'KEYWORD' [')'] component 'KEYWORD'
				'states' [ '(' , ')' ] collection ( ['|']
					'expression' [ '=' ] component 'conditional state group expression'
				)
		)

### conditional state group expression context path

	'conditional state group expression context path'
		'has steps' stategroup (
			'no'
			'yes' [ '$^' ]
				'tail' component 'conditional state group expression context path'
		)

### dictionary expression

	'dictionary expression'
		'head' component 'group context property selection'
		'type' stategroup (
			'prefiltered'
				'type' stategroup (
					'group' [ '+' ]
						'group' reference
					'state' [ '?' ]
						'state group' reference
						'state' [ '|' ] reference
				)
				'tail' component 'dictionary expression tail'
			'plural'
				'type' stategroup ( //NOTE: for dev compatible syntax
					'dictionary' [ '.' ]
					'matrix' [ '%' ]
				)
				'collection' reference
				'elementary key' stategroup ( 'elementary key' )
				'tail' component 'dictionary expression tail'
		)

### dictionary expression tail

	'dictionary expression tail'
		'head' component 'derivation node content path'
		'has steps' stategroup (
			'no'
			'yes'
				'type' stategroup ( //NOTE: for dev compatible syntax
					'dictionary' [ '.' ]
					'matrix' [ '%' ]
				)
				'collection' reference
				'elementary key' stategroup ( 'elementary key' )
				'tail' component 'dictionary expression tail'
		)

### node constraint

	'node constraint'

### traversed dictionary expression

	'traversed dictionary expression'
		'traversed head' component 'traversed derivation node content path'
		'step back' stategroup (
			'no'
			'yes'
				'type' stategroup (
					'dictionary' [ '.^' ]
					'matrix' [ '%^' ]
				)
				'constraint' component 'node constraint'
				'tail' component 'traversed dictionary expression'
		)

### referencer aggregate

	'referencer aggregate'
		'head' component 'group context property selection'
		'type' stategroup ( //NOTE: pipe for dev compatible syntax
			'prefiltered'
				'type' stategroup (
					'group' [ '+' ]
						'group' reference
					'state' [ '?' ]
						'state group' reference
						'state' [ '|' ] reference
				)
				'tail' component 'referencer aggregate step'
			'plural'
				'type' stategroup ( //NOTE: for dev compatible syntax
					'dictionary' [ '.' ]
					'matrix' [ '%' ]
				)
				'collection' reference
				'tail' component 'referencer aggregate step'
			'singular'
				'referencer type' stategroup (
					'matrix' [ '>key' ]
						'backward' stategroup ( 'backward' )
					'reference' [ '>' ]
						'reference' reference
						'backward' stategroup ( 'backward' )
				)
		)

### referencer aggregate step

	'referencer aggregate step'
		'head' component 'derivation node content path'
		'has steps' stategroup (
			'no'
				'referencer type' stategroup (
					'matrix' [ '>key' ]
						'backward' stategroup ( 'backward' )
					'reference' [ '>' ]
						'reference' reference
						'backward' stategroup ( 'backward' )
				)
			'yes'
				'type' stategroup ( //NOTE: for dev compatible syntax
					'dictionary' [ '.' ]
					'matrix' [ '%' ]
				)
				'collection' reference
				'tail' component 'referencer aggregate step'
		)

### numerical type constraint

	'numerical type constraint'

### numerical type conversion

	'numerical type conversion'
		'conversion' stategroup (
			'none'
				'constraint' component 'numerical type constraint'
			'factor'
				'conversion' ['from'] reference
			'base'
				'conversion' ['from' 'base'] reference
		)

### calculated signed number selection starting from property

	'calculated signed number selection starting from property'
		'sign' stategroup (
			'negative' [ '-' ]
			'positive'
		)
		'type' stategroup (
			'input parameter'
				'context selection' component 'ancestor node selection'
				'state' stategroup ( 'state' )
				'input parameter' [ '&#' ] reference
			'number from property'
				'context selection' component 'context property selection'
				'number' [ '#' ] reference
			'number from node'
				'selection' component 'calculated node selection starting from property'
				'number' [ '#' ] reference
		)

### signed number property list

	'signed number property list'
		'selection' component 'calculated signed number selection starting from property'
		'conversion' component 'numerical type conversion'
		'has element' stategroup (
			'no'
			'yes' [',']
				'tail' component 'signed number property list'
		)

### natural number property list

	'natural number property list'
		'selected number type' stategroup (
			'natural'
			'integer' [ 'unsafe' ]
		)
		'selection' component 'calculated signed number selection starting from property'
		'conversion' component 'numerical type conversion'
		'has element' stategroup (
			'no'
			'yes' [',']
				'tail' component 'natural number property list'
		)

### conditional number expression context path

	'conditional number expression context path'
		'has steps' stategroup (
			'no'
			'yes' [ '$^' ]
				'tail' component 'conditional number expression context path'
		)

### conditional number expression

	'conditional number expression'
		'has steps' stategroup (
			'no'
				'type' stategroup (
					'value' [ 'zero' ]
					'number'
						'expression context' component 'conditional number expression context path'
						'context' stategroup (
							'target context' [ '$^' ]
								'selection' component 'calculated signed number selection starting from property'
								'conversion' component 'numerical type conversion'
							'expression result'
								'sign' stategroup (
									'negative' [ '-' ]
									'positive'
								)
								'type' [ '$' ] stategroup ( //NOTE: keyword '$' is temporary
									'numerical input parameter'
										'input parameter' [ '&#' ] reference
										'conversion' component 'numerical type conversion'
									'number from node'
										'context type' stategroup (
											'input parameter'
												'input parameter' [ '&' ] reference
											'this state'
										)
										'selection' component 'calculated descendant node selection starting from node'
										'number' [ '#' ] reference
										'conversion' component 'numerical type conversion'
								)
						)
				)
			'yes' ['switch' '(']
				'expression context' component 'conditional number expression context path'
				'type' stategroup (
					'merge' [ '$^' ]
						'state group selection' component 'calculated state group selection starting from property'
					'flatten' ['$']
						'context type' stategroup (
							'input parameter'
								'input parameter' [ '&' ] reference
							'this state'
						)
						'selection' component 'calculated descendant node selection starting from node'
						'state group' [ '?' ] reference
				)
				'KEYWORD' [')'] component 'KEYWORD'
				'states' [ '(' , ')' ] collection ( ['|']
					'expression' [ '=' ] component 'conditional number expression'
				)
		)

### conditional natural number expression context path

	'conditional natural number expression context path'
		'has steps' stategroup (
			'no'
			'yes' [ '$^' ]
				'tail' component 'conditional natural number expression context path'
		)

### conditional natural number expression

	'conditional natural number expression'
		'has steps' stategroup (
			'no'
				'type' stategroup (
					'value' [ 'one' ]
					'number'
						'selected number type' stategroup (
							'natural'
							'integer' [ 'unsafe' ]
						)
						'expression context' component 'conditional natural number expression context path'
						'context' stategroup (
							'target context' [ '$^' ]
								'selection' component 'calculated signed number selection starting from property'
								'conversion' component 'numerical type conversion'
							'expression result'
								'type' [ '$' ] stategroup ( //NOTE: keyword '$' is temporary
									'numerical input parameter'
										'input parameter' [ '&#' ] reference
										'conversion' component 'numerical type conversion'
									'number from node'
										'context type' stategroup (
											'input parameter'
												'input parameter' [ '&' ] reference
											'this state'
										)
										'selection' component 'calculated descendant node selection starting from node'
										'number' [ '#' ] reference
										'conversion' component 'numerical type conversion'
								)
						)
				)
			'yes' ['switch' '(']
				'expression context' component 'conditional natural number expression context path'
				'type' stategroup (
					'merge' [ '$^' ]
						'state group selection' component 'calculated state group selection starting from property'
					'flatten' ['$']
						'context type' stategroup (
							'input parameter'
								'input parameter' [ '&' ] reference
							'this state'
						)
						'selection' component 'calculated descendant node selection starting from node'
						'state group' [ '?' ] reference
				)
				'KEYWORD' [')'] component 'KEYWORD'
				'states' [ '(' , ')' ] collection ( ['|']
					'expression' [ '=' ] component 'conditional natural number expression'
				)
		)

### integer expression

	'integer expression'
		'type' stategroup (
			'singular'
				'type' stategroup (
					'value' [ 'deprecated' ]
						'value' number
					'expression'
						'expression' component 'calculated signed number selection starting from property'
				)
			'conditional' ['switch']
				'state group selection' ['(',')'] component 'calculated state group selection starting from property'
				'states' [ '(' , ')' ] collection ( ['|']
					'expression' [ '=' ] component 'conditional number expression'
				)
			'referencer anchor sum' [ 'sum' ]
				'context selection' component 'entity scoped context property selection'
				'referencer anchor' [ '<' ] reference
				'filter' component 'derivation node content path'
				'number context selection' component 'entity scoped context node selection'
				'number' [ '#' ] reference
				'conversion' component 'numerical type conversion'
			'referencer anchor count' [ 'count' ]
				'context selection' component 'entity scoped context property selection'
				'referencer anchor' [ '<' ] reference
				'filter' component 'derivation node content path'
			'sum' [ 'sum' ]
				'collection selection' component 'calculated collection selection starting from property'
				'filter' component 'derivation node content path'
				'property' [ '#' ] reference
				'conversion' component 'numerical type conversion'
			'count' [ 'count' ]
				'collection selection' component 'calculated collection selection starting from property'
				'filter' component 'derivation node content path'
			'remainder' [ 'remainder' ]
				'numerator' [ '(' ] component 'calculated signed number selection starting from property'
				'conversion rule' ['as'] reference
				'numerator conversion' component 'numerical type conversion'
				'denominator set' [ ',' ] stategroup (
					'integer' [ 'unsafe' ]
					'natural'
				)
				'denominator' component 'calculated signed number selection starting from property'
				'denominator conversion' component 'numerical type conversion'
				'KEYWORD' [')'] component 'KEYWORD'
			'division' [ 'division' ]
				'rounding' stategroup (
					'ordinary'
					'ceil' [ 'ceil' ]
					'floor' [ 'floor' ]
				)
				'numerator' [ '(' ] component 'calculated signed number selection starting from property'
				'conversion rule' ['as'] reference
				'numerator conversion' component 'numerical type conversion'
				'denominator set' [ ',' ] stategroup (
					'integer' [ 'unsafe' ]
					'natural'
				)
				'denominator' component 'calculated signed number selection starting from property'
				'denominator conversion' component 'numerical type conversion'
				'KEYWORD' [')'] component 'KEYWORD'
			'product' [ 'product' ]
				'left' [ '(' ] component 'calculated signed number selection starting from property'
				'conversion rule' ['as'] reference
				'left conversion' component 'numerical type conversion'
				'right' [ ',' ] component 'calculated signed number selection starting from property'
				'right conversion' component 'numerical type conversion'
				'KEYWORD' [')'] component 'KEYWORD'
			'list operation'
				'operation' stategroup (
					'sum' [ 'sumlist' ]
					'maximum' [ 'max' ]
					'minimum' [ 'min' ]
				)
				'numbers' [ '(' , ')' ] component 'signed number property list'
			'addition' ['add' '(']
				'left' component 'calculated signed number selection starting from property'
				'left conversion' component 'numerical type conversion'
				'right' [ ',' ] component 'calculated signed number selection starting from property'
				'right conversion' component 'numerical type conversion'
				'KEYWORD' [')'] component 'KEYWORD'
			'difference' ['diff']
				'left' [ '(' ] component 'calculated signed number selection starting from property'
				'left constraint' component 'numerical type constraint'
				'right' [ ',' ] component 'calculated signed number selection starting from property'
				'right conversion' component 'numerical type conversion'
				'KEYWORD' [')'] component 'KEYWORD'
		)

### natural expression

	'natural expression'
		'type' stategroup (
			'singular'
				'type' stategroup (
					'value' [ 'deprecated' ]
						'value' number
					'expression'
						'selected number type' stategroup (
							'integer' [ 'unsafe' ]
							'natural'
						)
						'expression' component 'calculated signed number selection starting from property'
				)
			'conditional' ['switch']
				'state group selection' ['(' , ')'] component 'calculated state group selection starting from property'
				'states' [ '(' , ')' ] collection ( ['|']
					'expression' [ '=' ] component 'conditional natural number expression'
				)
			'referencer anchor sum' [ 'sum' 'unsafe' ]
				'context selection' component 'entity scoped context property selection'
				'referencer anchor' [ '<' ] reference
				'filter' component 'derivation node content path'
				'number context selection' component 'entity scoped context node selection'
				'number' [ '#' ] reference
				'conversion' component 'numerical type conversion'
			'referencer anchor count' [ 'count' 'unsafe' ]
				'context selection' component 'entity scoped context property selection'
				'referencer anchor' [ '<' ] reference
				'filter' component 'derivation node content path'
			'sum' [ 'sum' 'unsafe' ]
				'collection selection' component 'calculated collection selection starting from property'
				'filter' component 'derivation node content path'
				'property' [ '#' ] reference
				'conversion' component 'numerical type conversion'
			'count' [ 'count' 'unsafe' ]
				'collection selection' component 'calculated collection selection starting from property'
				'filter' component 'derivation node content path'
			'remainder' [ 'remainder' 'unsafe' ]
				'numerator' [ '(' ] component 'calculated signed number selection starting from property'
				'conversion rule' ['as'] reference
				'numerator conversion' component 'numerical type conversion'
				'denominator set' [ ',' ] stategroup (
					'integer' [ 'unsafe' ]
					'natural'
				)
				'denominator' component 'calculated signed number selection starting from property'
				'denominator conversion' component 'numerical type conversion'
				'KEYWORD' [')'] component 'KEYWORD'
			'division' [ 'division' ]
				'rounding' stategroup (
					'ordinary' [ 'unsafe' ]
					'ceil' [ 'ceil' ]
					'floor' [ 'floor' 'unsafe' ]
				)
				'numerator type' [ '(' ] stategroup (
					'integer' [ 'unsafe' ]
					'natural'
				)
				'numerator' component 'calculated signed number selection starting from property'
				'conversion rule' ['as'] reference
				'numerator conversion' component 'numerical type conversion'
				'denominator type' [ ',' ] stategroup (
					'integer' [ 'unsafe' ]
					'natural'
				)
				'denominator' component 'calculated signed number selection starting from property'
				'denominator conversion' component 'numerical type conversion'
				'KEYWORD' [')'] component 'KEYWORD'
			'product' [ 'product' ]
				'left number type' [ '(' ] stategroup (
					'integer' [ 'unsafe' ]
					'natural'
				)
				'left' component 'calculated signed number selection starting from property'
				'conversion rule' ['as'] reference
				'left conversion' component 'numerical type conversion'
				'right number type' [ ',' ] stategroup (
					'integer' [ 'unsafe' ]
					'natural'
				)
				'right' component 'calculated signed number selection starting from property'
				'right conversion' component 'numerical type conversion'
				'KEYWORD' [')'] component 'KEYWORD'
			'list operation'
				'operation' stategroup (
					'sum' [ 'sumlist' ]
					'maximum' [ 'max' ]
					'minimum' [ 'min' ]
				)
				'numbers' [ '(' , ')' ] component 'natural number property list'
			'addition' ['add']
				'left number type' ['('] stategroup (
					'integer' [ 'unsafe' ]
					'natural'
				)
				'left' component 'calculated signed number selection starting from property'
				'left conversion' component 'numerical type conversion'
				'right number type' [','] stategroup (
					'integer' [ 'unsafe' ]
					'natural'
				)
				'right' component 'calculated signed number selection starting from property'
				'right conversion' component 'numerical type conversion'
				'KEYWORD' [')'] component 'KEYWORD'
			'difference' [ 'diff' 'unsafe' ]
				'left' ['('] component 'calculated signed number selection starting from property'
				'left constraint' component 'numerical type constraint'
				'right' [','] component 'calculated signed number selection starting from property'
				'right conversion' component 'numerical type conversion'
				'KEYWORD' [')'] component 'KEYWORD'
		)

### text selection starting from property

	'text selection starting from property'
		'type' stategroup (
			'value'
				'value' text
			'text'
				'type' stategroup (
					'text'
						'context selection' component 'context property selection'
						'text' [ '.' ] reference
					'node'
						'selection' component 'calculated node selection starting from property'
						'text' [ '.' ] reference
				)
			'id'
				'type' stategroup (
					'ancestor'
						'selection' component 'context property selection'
					'node'
						'selection' component 'calculated node selection starting from property'
				)
				'collection type' stategroup (
					'dictionary' [ '.key' ]
					// 'matrix' [ '%id' ]
				)
		)

### conditional text expression context path

	'conditional text expression context path'
		'has steps' stategroup (
			'no'
			'yes' [ '$^' ]
				'tail' component 'conditional text expression context path'
		)

### conditional text expression

	'conditional text expression'
		'has steps' stategroup (
			'no'
				'type' stategroup (
					'value'
						'value' text
					'text'
						'expression context' component 'conditional text expression context path'
						'context' stategroup (
							'target context' [ '$^' ]
								'selection' component 'text selection starting from property'
							'expression result' [ '$' ] //NOTE: keyword '$' is temporary
								'context type' stategroup (
									'input parameter'
										'input parameter' [ '&' ] reference
									'this state'
								)
								'selection' component 'calculated descendant node selection starting from node'
								'type' stategroup (
									'text'
										'text' [ '.' ] reference
									'id'
										'collection type' stategroup (
											'dictionary' [ '.key' ]
											// 'matrix' [ '%id' ]
										)
								)
						)
				)
			'yes' ['switch' '(']
				'expression context' component 'conditional text expression context path'
				'type' stategroup (
					'merge' [ '$^' ]
						'state group selection' component 'calculated state group selection starting from property'
					'flatten' ['$']
						'context type' stategroup (
							'input parameter'
								'input parameter' [ '&' ] reference
							'this state'
						)
						'selection' component 'calculated descendant node selection starting from node'
						'state group' [ '?' ] reference
				)
				'KEYWORD' [')'] component 'KEYWORD'
				'states' [ '(' , ')' ] collection ( ['|']
					'expression' [ '=' ] component 'conditional text expression'
				)
		)

### text expression

	'text expression'
		//NOTE: result node is an ugly way to enforce a location on type==id
		'type' stategroup (
			'singular'
				'selection' component 'text selection starting from property'
			'conditional' ['switch' ]
				'state group selection' ['(', ')'] component 'calculated state group selection starting from property'
				'states' [ '(' , ')' ] collection ( ['|']
					'expression' [ '=' ] component 'conditional text expression'
				)
		)
		'has successor' stategroup (
			'no'
			'yes'
				'tail' component 'text expression'
		)

### conditional file expression context path

	'conditional file expression context path'
		'has steps' stategroup (
			'no'
			'yes' [ '$^' ]
				'tail' component 'conditional file expression context path'
		)

### conditional file expression

	'conditional file expression'
		'has steps' stategroup (
			'no'
				'expression context' component 'conditional file expression context path'
				'context' stategroup (
					'target context' [ '$^' ]
						'type' stategroup (
							'property'
								'context selection' component 'context property selection'
								'file' [ '/' ] reference
							'node'
								'selection' component 'calculated node selection starting from property'
								'file' [ '/' ] reference
						)
					'expression result' [ '$' ] //NOTE: keyword '$' is temporary
						'context type' stategroup (
							'input parameter'
								'input parameter' [ '&' ] reference
							'this state'
						)
						'selection' component 'calculated descendant node selection starting from node'
						'file' [ '/' ] reference
				)
			'yes' ['switch' '(']
				'expression context' component 'conditional file expression context path'
				'type' stategroup (
					'merge' [ '$^' ]
						'state group selection' component 'calculated state group selection starting from property'
					'flatten' ['$']
						'context type' stategroup (
							'input parameter'
								'input parameter' [ '&' ] reference
							'this state'
						)
						'selection' component 'calculated descendant node selection starting from node'
						'state group' [ '?' ] reference
				)
				'KEYWORD' [')'] component 'KEYWORD'
				'states' [ '(' , ')' ] collection ( ['|']
					'expression' [ '=' ] component 'conditional file expression'
				)
		)

### key

	'key'

### KEYWORD

	'KEYWORD'

### node

	'node' [ '{' , '}' ]
		'work' stategroup (
			'no'
			'yes'
				'role' [ 'workfor' ] reference
		)
		'attributes' collection (
			'preceding siblings' collection predecessors
			'type' stategroup (
				'referencer anchor'[':' 'reference-set']
					'node context' ['->'] component 'node path'
					'EQ node type' component 'EQ node type'
					'referencer type' ['=>' 'inverse'] stategroup (
						'key' ['>key' ]
						'reference'
							'reference' [ '>' ] reference
					)
				'log' [ ':' 'log' ]
					'root' component 'log node'
				'command' [ ':' 'command' ]
					'type' stategroup (
						'global'
						'component' [ 'component' ]
					)
					'parameters' component 'command parameters'
					'implementation' stategroup (
						'external' [ 'external' ]
							'interface' [ 'from' ] reference
						'internal'
							'implementation' component 'command implementation'
					)
				'property'
					'mutation permission' stategroup (
						'inherited'
						'defined'
							'definition' component 'mutation permission definition'
					)
					'read permission' stategroup (
						'inherited'
						'defined'
							'definition' component 'read permission definition'
					)
					'data type' stategroup (
						'elementary' [ ':' ]
						'derived' [ ':=' ]
					)
					'type' stategroup (
						'group' [ 'group' ]
							'type' stategroup (
								'elementary'
									'elementary value' component 'elementary value'
								'derived' ['=']
									'derived value' component 'derived value'
							)
							'node' component 'node'
						'reference' [ 'text' ]
							'type' stategroup (
								'elementary'
									'elementary value' component 'elementary value'
									'referencer' [ '->' ] group (
										'type' stategroup (
											'backward'
												'backward' component 'backward selection'
												'selection' component 'resolved collection selection starting from property'
											'forward' [ 'forward' ]
												'head' component 'unresolved node selection'
												'type' stategroup (
													'dictionary' [ '.' ]
													'matrix' [ '%' ]
												)
												'collection' reference
												'constrain' stategroup (
													'no'
														'forward' component 'forward selection'
													'yes' ['/']
														'backward' component 'backward selection'
														'ancestor' component 'ancestor node selection'
														'collection constraint' reference
												)
										)
										'tail' component 'node content path'
										'bidirectional' stategroup (
											'no'
											'yes' [ '-<' ]
												'anchor' reference
										)
									)
									'record mutation time' stategroup (
										'yes' ['mutation-time']
											'meta property' ['=' '#'] reference
										'no'
									)
								'derived' ['=>']
									'derived value' component 'derived value'
									'referencer' ['(' , ')'] group (
											'type' stategroup (
												'backward'
													'backward' component 'backward selection'
													'selection' component 'calculated collection selection starting from property'
													'tail' component 'derivation node content path'
												'self'
													'forward' component 'forward selection'
													'selection' component 'ancestor node selection'
													'type' stategroup (
														'dictionary' [ '.self' ]
													)
												//'forward' [ 'forward' ]
												//	'forward' component 'forward selection'
												//	'ancestor node selection' component 'ancestor node selection'
												//	'group node selection' component 'group node selection'
												//	'type' stategroup ( //NOTE: for for dev compatible syntax
												//		'dictionary' [ '.' ]
												//		'matrix' [ '%' ]
												//	)
												//	'collection' reference
											)
										)
										'type' stategroup (
											'dictionary branch'
												'branch' [ 'from' ] reference
												'root entity constraint' stategroup ( 'root' )
												'expression' [ '[', ']' ] component 'calculated node selection starting from property'
											'singular'
												'expression' component 'calculated node selection starting from property'
										)
							)
							'output parameters' collection ( [ '(' , ')' ]
								'dependable' component 'dependency'
								'type' stategroup (
									'elementary' [ '->' ]
										'head' component 'entity scoped context node selection'
										'selection' component 'resolved node descendant selection starting from node'
									'derived' [ '=>' ]
										'head' component 'entity scoped context node selection'
										'context type' stategroup (
											'input parameter' [ '&' ]
												'input parameter' reference
											'result node'
										)
										'selection' component 'calculated descendant node selection starting from node'
								)
							)
							'referencer' component 'referencer'
						'dictionary' [ 'collection' ]
							'type' stategroup (
								'elementary'
									'elementary value' component 'elementary value'
									'constraints' component 'constraints'
								'derived' [ '=' 'union' ]
									'derived value' component 'derived value'
									'branches' ['(', ')'] collection (
										'expression' [ '=' ] component 'dictionary expression'
									)
									'separator' ['join'] stategroup (
										'dot' ['.']
										'dash' ['-']
										'colon' [':']
										'greater than' ['>']
										'space' ['space']
									)
							)
							'key' component 'key'
							'key type' stategroup (
								'link' [ '~>' ]
									'selection' component 'link text expression'
								'simple'
							)
							'entity' component 'entity'
							'node' component 'node'
						'matrix' [ 'collection' ]
							'type' stategroup (
								'elementary'
									'elementary value' component 'elementary value'
									'referencer' [ '->' ] group (
										'type' stategroup (
											'backward'
												'backward' component 'backward selection'
												'selection' component 'resolved collection selection starting from property'
											'forward' [ 'forward' ]
												'head' component 'unresolved node selection'
												'type' stategroup (
													'dictionary' [ '.' ]
													'matrix' [ '%' ]
												)
												'collection' reference
												'constrain' stategroup (
													'no'
														'forward' component 'forward selection'
													'yes'['/']
														'backward' component 'backward selection'
														'ancestor selection' component 'ancestor node selection' //TODO: remove
														'collection constraint' reference
												)
										)
										'tail' component 'node content path'
										'elementary' stategroup ( 'elementary' )
										'bidirectional' stategroup (
											'no'
											'yes' [ '-<' ]
												'anchor' reference
										)
									)
									'constraints' component 'constraints'
								'derived'
									'derived value' component 'derived value'
									'referencer' [ '=>' ] group (
										'type' stategroup (
											'backward'
												'backward' component 'backward selection'
												'selection' component 'calculated collection selection starting from property'
											//'forward' [ 'forward' ]
											//	'forward' component 'forward selection'
											//	'head' component 'uncalculated context node selection'
											//	'type' stategroup ( //NOTE: for dev compatible syntax
											//		'dictionary' [ '.' ]
											//		'matrix' [ '%' ]
											//	)
											//	'collection' reference
										)
										'tail' component 'derivation node content path'
									)
									'type' stategroup (
										'augment'
										'merge' [ 'in' ]
											'aggregates' [ '(' , ')' ] collection (
												'aggregate' [ '=>' ] component 'referencer aggregate'
											)
									)
							)
							'output parameters' collection ( [ '(' , ')' ]
								'dependable' component 'dependency'
								'type' stategroup (
									'elementary' [ '->' ]
										'head' component 'entity scoped context node selection'
										'selection' component 'resolved node descendant selection starting from node'
									'derived' [ '=>' ]
										'head' component 'entity scoped context node selection'
										'context type' stategroup (
											'input parameter' [ '&' ]
												'input parameter' reference
											'result node'
										)
										'selection' component 'calculated descendant node selection starting from node'
								)
							)
							'referencer' component 'referencer'
							'entity' component 'entity'
							'node' component 'node'
						'number'
							'type' stategroup (
								'elementary'
									'elementary value' component 'elementary value'
									'set' stategroup (
										'integer' [ 'integer' ]
										'natural' [ 'natural' ]
									)
									'numerical type' reference
									'type' stategroup (
										'causal'
											'type' stategroup (
												'mutation' [ '=' 'mutation-time' ]
													'watched property' stategroup (
														'reference' [ '>' ]
															'reference' reference
														'number' [ '#' ]
															'number' reference
														'text' [ '.' ]
															'text' reference
													)
												'creation' [ '=' 'creation-time' ]
												'destruction'
													'destruction operation' stategroup (
														'set to lifetime' [ '=' 'life-time' ]
														'add lifetime' [ 'add' 'life-time' ]
														'subtract lifetime' [ 'subtract' 'life-time' ] //TODO: drop? we don't need this.
													)
													'watched stategroup' ['?'] reference
													'watched state' ['|'] reference
											)
										'simple'
											'record mutation time' stategroup ( //use triggers instead, to set mutation time with 'now'?
												'yes' ['mutation-time']
													'meta property' ['=' '#'] reference
												'no'
											)
									)
								'derived'
									'derived value' component 'derived value'
									'type' stategroup (
										'integer' [ 'integer' ]
											'numerical type' reference
											'conversion' [ '=' ] stategroup (
												'none'
												'singular'
													'conversion rule' ['from'] reference
											)
											'expression' component 'integer expression'
										'natural' [ 'natural' ]
											'numerical type' reference
											'conversion' [ '=' ] stategroup (
												'none'
												'singular'
													'conversion rule' ['from'] reference
											)
											'expression' component 'natural expression'
									)
							)
							'behaviour' stategroup (
								'none'
								'timer' [ 'timer']
									'timeout operation node' [ 'ontimeout' ] component 'context node selection'
									'timeout operation' [ 'update' ] component 'update node'
							)
						'file' ['file']
							'type' stategroup (
								'elementary'
									'elementary value' component 'elementary value'
								'derived' [ '=' ]
									'derived value' component 'derived value'
									'type' stategroup (
										'singular'
											'type' stategroup (
												'property'
													'context selection' component 'context property selection'
													'file' [ '/' ] reference
												'node'
													'selection' component 'calculated node selection starting from property'
													'file' [ '/' ] reference
											)
										'conditional' ['switch']
											'state group selection' ['(',')'] component 'calculated state group selection starting from property'
											'states' [ '(' , ')' ] collection ( ['|']
												'expression' [ '=' ] component 'conditional file expression'
											)
									)
							)
						'text' ['text']
							'type' stategroup (
								'elementary'
									'elementary value' component 'elementary value'
									'record mutation time' stategroup (
										'yes' ['mutation-time']
											'meta property' ['=' '#'] reference
										'no'
									)
								'derived'
									'derived value' component 'derived value'
									'expression' [ '=' ] component 'text expression'
							)
							'value type' stategroup (
								'link' [ '~>' ]
									'selection' component 'link text expression'
								'simple'
							)
						'state group' [ 'stategroup' ]
							'type' stategroup (
								'elementary'
									'elementary value' component 'elementary value'
								'derived' ['=']
									'derived value' component 'derived value'
									'expression type' stategroup (
										'resolvable link' [ 'any' ]
											'link context selection' ['('] component 'context property selection'
											'link type' stategroup (
												'text'
													'text' [ '>' ] reference
												'key' [ '>key' ]
											)
											'KEYWORD' [')'] component 'KEYWORD'
											'yes state instantiation' [ '(' '|' 'true' '=' ] group (
												'state' reference
												'input arguments' collection ( [ '(' , ')' ]
													'type' [ '=>' ] stategroup (
														'target context'
															'selection' component 'calculated node selection starting from property'
														'expression result'
															'expression context path' component 'link text expression context path'
															'state input parameter' stategroup (
																'yes' [ '&' ]
																	'input parameter' reference
																'no'
															)
															'entity node selection' component 'entity scoped context node selection'
															'selection' component 'calculated descendant node selection starting from node'
													)
												)
											)
											'no state instantiation' [ '|' 'false' '=' ] component 'state instantiation'
											'KEYWORD2' [')'] component 'KEYWORD'
										'dictionary branch' [ 'match-branch' ]
											'branches' ['(', ')'] collection ( ['|']
												'state instantiation' [ '=' ] group (
													'state' reference
													'input arguments' collection ( [ '(' , ')' ]
														'type' [ '=>' ] stategroup (
															'target context'
																'selection' component 'calculated node selection starting from property'
															'expression result' [ '$' ]
																'expression context path' component 'traversed dictionary expression'
																'state input parameter' stategroup (
																	'yes' [ '&' ]
																		'input parameter' reference
																	'no'
																)
																'selection' component 'calculated descendant node selection starting from node'
														)
													)
												)
											)
										'matrix contains' ['any' '(']
											'collection selection' component 'calculated collection selection starting from property'
											'matrix' stategroup ( 'matrix' )
											'key' [ '[' ,']' ] component 'calculated node selection starting from property'
											'yes state instantiation' [ ')' '(' '|' 'true' '=' ] component 'state instantiation 2'
											'no state instantiation' [ '|' 'false' '=' ] component 'state instantiation'
											'KEYWORD' [')'] component 'KEYWORD'
										'node equality' ['match' '(']
											'left node type' stategroup (
												'ancestor'
													'selection' component 'ancestor node selection'
												'sibling'
													'selection' component 'calculated node selection starting from property'
											)
											'right node' [ '==' ] component 'calculated node selection starting from property'
											'yes state instantiation' [ ')' '(' '|' 'true' '=' ] component 'state instantiation 2'
											'no state instantiation' [ '|' 'false' '=' ] component 'state instantiation 2'
											'KEYWORD' [')'] component 'KEYWORD'
										'numerical' ['match']
											'left expression' ['('] component 'calculated signed number selection starting from property'
											'operator' stategroup (
												'equal to' [ '==' ]
												'greater than' [ '>' ]
												'greater than or equal to' [ '>=' ]
												'smaller than' [ '<' ]
												'smaller than or equal to' [ '<=' ]
											)
											'right type' stategroup (
												'value'
													'value' stategroup (
														'zero' [ 'zero' ]
														'one' [ 'one' ]
													)
												'expression'
													'right expression' component 'calculated signed number selection starting from property'
													'right conversion' component 'numerical type conversion'
											)
											'yes state instantiation' [ ')' '(' '|' 'true' '=' ] component 'state instantiation'
											'no state instantiation' [ '|' 'false' '=' ] component 'state instantiation'
											'KEYWORD' [')'] component 'KEYWORD'
										'state merge' ['switch']
											'state group selection' [ '(' , ')' ] component 'calculated state group selection starting from property'
											'states' [ '(' , ')' ] collection ( ['|']
												'expression' [ '=' ] component 'conditional state group expression'
											)
										'aggregation emptiness' [ 'any' ]
											'aggregate' [ '(' , ')' ] group ( //TODO: remove this group
												'collection selection' component 'calculated collection selection starting from property'
												'filter' component 'derivation node content path'
											)
											'no state instantiation' [ '(' '|' 'true' '=' ] group (
												'state' reference
												'input arguments' collection ( [ '(' , ')' ]
													'type' stategroup (
														'node' [ '=>' ]
															'selection' component 'calculated node selection starting from property'
														'number'
															'operation' [ '=' ] stategroup (
																'minimum' [ 'min' ]
																'maximum' [ 'max' ]
																'standard deviation' [ 'std' ]
															)
															'expression' group (
																'descendant selection' [ '$' ] component 'calculated descendant node selection starting from node'
																'number' [ '#' ] reference
															)
													)
												)
											)
											'yes state instantiation' [ '|' 'false' '=' ] component 'state instantiation' //NOTE: no = yes, and yes = no for syntax migration.
											'KEYWORD' [')'] component 'KEYWORD'
									)
							)
							'output parameters' collection ( [ '(' , ')' ]
								'dependable' component 'dependency'
								'type' stategroup (
									'elementary' [ '->' ]
									'derived' [ '=>' ]
								)
								'node selection' component 'node path'
							)
							'states' [ '(' , ')' ] collection indent (
								'record lifetime' stategroup (
									'yes' ['life-time']
										'meta property' ['=' '#'] reference
										'creation timestamp' ['from'] reference
									'no'
									)
								'input parameters' collection ( [ '(' , ')' ]
									'type' stategroup (
										'node'
											'type' stategroup (
												'elementary' ['->']
													'selection' component 'resolved state group selection starting from property'
													'state' [ '|' ] reference
													'tail' component 'node content path'
												'derived' [':']
													'node selection' component 'node path'
											)
										'number'
											'set' [':'] stategroup (
												'integer' ['integer']
												'natural' ['natural']
											)
											'numerical type' reference
									)
								)
								'output arguments' [ '->' ] collection ( [ '(' , ')' ]
									'type' stategroup (
										'elementary' [ '->' ]
											'type' stategroup (
												'descendant'
													'type' stategroup (
														'input parameter' ['&']
															'input parameter' reference
														'this'
													)
													'selection' component 'resolved node descendant selection starting from node'
												'ancestor' [ '?^' ]
													'selection' component 'resolved node selection starting from property'
											)
										'derived' [ '=>' ]
											'type' stategroup (
												'descendant'
													'type' stategroup (
														'input parameter' ['&']
															'input parameter' reference
														'this'
													)
													'selection' component 'calculated descendant node selection starting from node'
												'ancestor' [ '?^' ]
													'selection' component 'calculated node selection starting from property'
											)
									)
								)
								'node' component 'node'
							)
					)
			)
		)

### EQ node type

	'EQ node type'

### link text expression

	'link text expression'
		'dependency' stategroup (
			'link'
				'context selection' component 'context property selection'
				'link type' stategroup (
					'text'
						'text' [ '.' ] reference //TODO: use > (ambiguous right now)
					'key' [ '.key' ] //TODO: use >key (ambiguous right now)
						'dictionary' stategroup ( 'dictionary' )
				)
				'group selection' component 'group node selection'
				'type' stategroup (
					'dictionary' [ '.' ]
						'dictionary' reference
					'matrix' [ '%' ]
						'matrix' reference
				)
			'node'
				'collection selection' component 'calculated collection selection starting from property'
		)
		'tail' component 'derivation node content path'

### link text expression context path

	'link text expression context path'
		'has steps' stategroup (
			'no' [ '$' ]
			'yes' [ '$^' ]
				'tail' component 'link text expression context path'
		)

### log node

	'log node' [ '(' , ')' ]
		'properties' collection (
			'type' [ ':' ] stategroup (
				'group' [ 'group' ]
					'node' component 'log node'
				'number' [ 'number' ]
				'reference' [ 'reference' ]
				'state group' [ 'stategroup' ]
					'states' [ '(' , ')' ] collection (
						'node' component 'log node'
					)
				'text' [ 'text' ]
				'file' ['file']
			)
		)

### delete node

	'delete node'

### new collection entries

	'new collection entries'
		'entries' collection (
			'node' component 'initialize node'
		)

### initialize node

	'initialize node' [ '(' , ')' ]
		'groups' collection (
			'node' [ ':' 'group' ] component 'initialize node'
		)
		'files' collection (
			'token' [':' 'file'] text
			'extension' text
		)
		'texts' collection (
			'value' [ ':' 'text' ] text
		)
		'numbers' collection (
			'type' [ ':' ] stategroup (
				'natural' [ 'natural' ]
					'value' number
				'integer' [ 'integer' ]
					'value' number
			)
		)
		'references' collection (
			'referenced node' [ ':' 'reference' ] text
		)
		'state groups' collection (
			'state' [ ':' 'stategroup' ] reference
			'node' component 'initialize node'
		)
		'dictionaries' collection (
			'entries' [ ':' 'dictionary' ] component 'new collection entries'
		)
		'matrices' collection (
			'entries' [ ':' 'matrix' ] component 'new collection entries'
		)

### update node

	'update node' [ '(' , ')' ]
		'properties' collection (
			'type' [ ':' ] stategroup (
				'collection'
					'type' stategroup (
						'dictionary' [ 'dictionary' ]
						'matrix' [ 'matrix' ]
					)
					'entries' collection (
						'type' stategroup (
							'rename' [ 'rename' ]
								'old id' [ 'from' ] reference
							'create' [ 'create' ]
								'node' component 'initialize node'
							'update' [ 'update' ]
								'invalidate referencer' stategroup (
									'no'
									'yes' [ 'invalidate' 'referencer' ]
								)
								'update node' component 'update node'
							'remove' [ 'remove' ]
								'delete node' component 'delete node'
						)
					)
				'group' [ 'group' ]
					'update node' component 'update node'
				'number'
					'type' stategroup (
						'natural' [ 'natural' ]
							'new value' number
						'integer' [ 'integer' ]
							'new value' number
					)
				'reference' [ 'reference' ]
					'new referenced node' text
				'state group' [ 'stategroup' ]
					'state' ['='] reference
					'type' stategroup (
						'set'
							'node' component 'initialize node'
							'delete node' component 'delete node'
						'update' [ 'update' ] //TODO: move 'state' here.
							'update node' component 'update node'
					)
				'text' [ 'text' ]
					'new value' text
				'file' ['file']
					'new token' text
					'new extension' ['.'] text
			)
		)

### creation context

	'creation context'

### creation

	'creation'
		'context' component 'creation context'

### command implementation

	'command implementation' ['do']
		'conditional' stategroup (
			'yes'
				'type' stategroup (
					'state switch' [ 'switch' '(' ]
						'state group' [ '@' , ')' ] reference
						'states' [ '(' , ')' ] collection ( ['|']
							'implementation' component 'command implementation'
						)
					'contains switch' ['any' '(']
						'context node path' component 'unconstrained node selection path'
						'type' stategroup (
							'dictionary'
								'dictionary' [ '.' ] reference
								'type' [ 'contains' '@' ] stategroup (
									'text'
										'text' reference
									'reference'
										'reference' reference
										'context node' component 'command parameter entity scoped context node selection'
										'dictionary' [ '.key' ] group ( )
								)
						)
						'yes case' [ ')' '(' 'true' ] component 'command implementation'
						'no case' [ 'false' ] component 'command implementation'
						'KEYWORD' [')'] component 'KEYWORD'
				)
			'no'
				'target' [ 'on' ] stategroup (
					'parameter'
						'parameter' [ '@' ] reference
					'context node'
						'context node path' component 'unconstrained node selection path'
				)
				'no creation context' component 'creation context'
				'update node' component 'parametrized update node'
		)

### node status

	'node status'

### command parameters

	'command parameters' [ '{' , '}' ]
		'properties' collection indent (
			'preceding siblings' collection predecessors
			'type' [ ':' ] stategroup (
				'matrix'
					'type' stategroup (
						'dense' [ 'collection' 'dense' ]
						'sparse' [ 'collection' 'sparse' ]
					)
					'referencer' [ '->' ] component 'command parameter referencer'
					'parameters' component 'command parameters'
				'reference' [ 'text' ]
					'referencer' [ '->' ] component 'command parameter referencer'
				'number'
					'set' stategroup (
						'integer' [ 'integer' ]
						'natural' [ 'natural' ]
					)
					'numerical type' reference
				'text' [ 'text' ]
				'file' ['file']
				'state group' [ 'stategroup' ]
					'states' [ '(' , ')' ] collection (
						'parameters' component 'command parameters'
					)
			)
		)

### context command parameters selection

	'context command parameters selection'
		'has steps' stategroup (
			'no'
			'yes'
				'type' stategroup (
					'state parent' [ '@?^' ]
					'matrix parent' [ '@%^' ]
				)
				'tail' component 'context command parameters selection'
		)

### context command parameter selection starting from parameter

	'context command parameter selection starting from parameter'
		'has steps' stategroup (
			'no'
			'yes'
				'type' stategroup (
					'state parent' [ '?^' ]
					'matrix parent' [ '%^' ]
				)
				'tail' component 'context command parameter selection starting from parameter'
		)

### command parameter referencer

	'command parameter referencer'
		'node status' stategroup (
			'new' [ 'new' ]
				'node status' component 'node status'
			'existing'
		)
		'context type' stategroup (
			'command parameter'
				'selection' component 'context command parameter selection starting from parameter'
				'type' stategroup (
					'sibling' [ '$' ]
						'reference' [ '>' ] reference
					'ancestor' [ '$' '>key' ]
				)
			'context node'
				'node status' component 'node status'
		)
		'head' component 'derivation selection path'
		'type' stategroup (
			'dictionary' [ '.' ]
				'dictionary' reference
			'matrix' [ '%' ]
				'matrix' reference
		)
		'tail' component 'derivation node content path'

### command parameter entity scoped context node selection

	'command parameter entity scoped context node selection'
		'has steps' stategroup (
			'no'
			'yes'
				'type' stategroup (
					'state parent' [ '?^' ]
					'group parent' [ '+^' ]
					'matrix key' [ '>key' ]
				)
				'tail' component 'command parameter entity scoped context node selection'
		)

### parametrized unconstrained node selection path

	'parametrized unconstrained node selection path'
		'context' stategroup (
			'this' [ '$' ]
			'command'
			'parameter'
				'selection' component 'context command parameters selection'
				'parameter' [ '@' ] reference
		)
		'path' component 'unconstrained node selection path'

### type eq

	'type eq'

### parametrized number expression

	'parametrized number expression'
		'type' stategroup (
			'binary expression'
				'operation' stategroup (
					'sum' [ 'sum' ]
						'type eq' component 'type eq'
					'difference' [ 'diff' ]
					'division' [ 'division' ]
						'rounding' stategroup (
							'ordinary'
							'ceil' [ 'ceil' ]
							'floor' [ 'floor' ]
						)
						'type eq' component 'type eq'
					'product' ['product']
						'type eq' component 'type eq'
					'min' ['min']
						'type eq' component 'type eq'
					'max' ['max']
						'type eq' component 'type eq'
				)
				'expressions' [ '(' , ')' ] group (
					'left' component 'parametrized number expression'
					'right' [','] component 'parametrized number expression'
				)
			'unary expression'
				'type' stategroup (
					'natural to integer cast' ['(' 'integer' ')']
						'expression' component 'parametrized number expression'
				)
			'property'
				'path' component 'parametrized unconstrained node selection path'
				'number' [ '#' ] reference
			'argument'
				'path' component 'context command parameters selection'
				'number' [ '@' ] reference
			'current timestamp' [ 'now' ]
			'static'
				'value' stategroup (
					'zero' [ 'zero' ]
					'one' [ 'one' ]
				)
		)

### command arguments

	'command arguments' [ '(' , ')' ]
		'properties' collection (
			'type' [ ':' ] stategroup (
				'matrix' [ 'collection' ]
					'source' ['=>'] stategroup (
						'argument'
							'selection' component 'context command parameters selection'
							'matrix' [ '@' ] reference
							'context selection' component 'command parameter entity scoped context node selection'
							'arguments' component 'command arguments'
						'property'
							'context' stategroup (
								'this' [ '$' ]
									'path' component 'unconstrained node selection path'
									'matrix' [ '%' ] reference
									'context selection' component 'command parameter entity scoped context node selection'
									'arguments' component 'command arguments'
								'calling command'
									'path' component 'unconstrained node selection path'
									'matrix' [ '%' ] reference
									'context selection' component 'command parameter entity scoped context node selection'
									'arguments' component 'command arguments'
							)
					)
				'reference' [ 'text' ]
					'source' ['=>'] stategroup (
						'created entry' [ 'created' 'entry' ]
							'entry' stategroup (
								'ancestor' [ '.^' ]
									'context selection' component 'ancestor node selection'
								'context'
									'type' stategroup (
										'this'
										'descendant'
											'parent reference' [ '$' '>' ] reference
											'head state constraint' component 'node content constraint'
											'type' stategroup (
												'dictionary'
													'dictionary' [ '.' ] reference
												'matrix'
													'matrix' [ '%' ] reference
											)
									)
									'node constraint' component 'node content constraint'
							)
						'new entry argument'
							'selection' component 'context command parameters selection'
							'reference' [ '@' 'new' ] reference
							'context node' component 'command parameter entity scoped context node selection'
						'node'
							'path' component 'parametrized unconstrained node selection path'
					)
				'number'
					'type' stategroup (
						'integer' [ 'integer' ]
						'natural' [ 'natural' ]
					)
					'expression' ['='] component 'parametrized number expression'
				'text' [ 'text' ]
					'source' ['='] stategroup (
						'argument'
							'selection' component 'context command parameters selection'
							'text' [ '@' ] reference
						'property'
							'path' component 'parametrized unconstrained node selection path'
							'type' stategroup (
								'text'
									'text' [ '.' ] reference
								'id' [ '.key' ]
							)
					)
				'file' ['file']
					'source' ['='] stategroup (
						'argument'
							'selection' component 'context command parameters selection'
							'file' [ '@' ] reference
						'property'
							'path' component 'parametrized unconstrained node selection path'
							'file' [ '/' ] reference
					)
				'state group' [ 'stategroup' ]
					'source' ['='] stategroup (
						'fixed'
							'state' reference
							'arguments' component 'command arguments'
						'property' ['switch']
							'context' stategroup (
								'this' [ '(' ]
									'path' ['$'] component 'unconstrained node selection path'
									'state group' ['?', ')'] reference
									'mapping' ['(', ')'] collection ( ['|']
										'mapped state' ['='] reference
										'arguments' component 'command arguments'
									)
								'calling command' [ '(' ]
									'path' component 'unconstrained node selection path'
									'state group' ['?' , ')'] reference
									'mapping' ['(', ')'] collection ( ['|']
										'mapped state' ['='] reference
										'arguments' component 'command arguments'
									)
							)
						'argument' ['switch']
							'selection' ['('] component 'context command parameters selection'
							'state group' ['@', ')'] reference
							'mapping' ['(', ')'] collection ( ['|']
								'mapped state' ['='] reference
								'arguments' component 'command arguments'
							)
					)
			)
		)

### node content constraint

	'node content constraint'
		'has steps' stategroup (
			'no'
			'yes'
				'type' stategroup (
					'state'
						'state group' [ '?' ] reference
					'group'
						'group' [ '+' ] reference
				)
				'tail' component 'node content constraint'
		)

### parametrized update node

	'parametrized update node' [ '(' , ')' ]
		'attributes' collection indent (
			'type' stategroup (
				'command'
					'arguments' [ 'with' ] component 'command arguments'
				'property' [ ':' ]
					'type' stategroup (
						'collection'
							'type' stategroup (
								'dictionary' ['dictionary']
									'type' stategroup (
										'create' [ 'create' ]
											'key source' stategroup (
												'argument'
													'selection' component 'context command parameters selection'
													'text' [ '@' ] reference
												'node'
													'path' component 'parametrized unconstrained node selection path'
													'dictionary' [ '.key' ] stategroup ( 'dictionary' )
											)
											'initialize node' component 'parametrized initialize node'
											'has update block' stategroup (
												'no'
												'yes' ['and' 'on']
													'path' component 'parametrized unconstrained node selection path'
													'creation' component 'creation'
													'update node' component 'parametrized update node'
											)
										'delete' ['delete']
											'selection' component 'context command parameters selection'
											'entry' [ '@' ] reference
											'delete node' component 'delete node'
									)
								'matrix' ['matrix']
									'type' stategroup (
										'create' [ 'create' ]
											'selection' component 'context command parameters selection'
											'reference' [ '@' ] reference
											'context node' component 'command parameter entity scoped context node selection'
											'initialize node' component 'parametrized initialize node'
											'has update block' stategroup (
												'no'
												'yes' ['and' 'on']
													'path' component 'parametrized unconstrained node selection path'
													'creation' component 'creation'
													'update node' component 'parametrized update node'
											)
										'delete' ['delete']
											'selection' component 'context command parameters selection'
											'entry' ['@'] reference
											'delete node' component 'delete node'
									)
							)
						'number'
							'set' stategroup (
								'integer' [ 'integer' ]
								'natural' [ 'natural' ]
							)
							'operator' stategroup (
								'increment' [ 'increment' ]
								'add'
									'selection' [ 'add' ] component 'context command parameters selection'
									'number' [ '@' ] reference
								'subtract'
									'selection' [ 'subtract' ] component 'context command parameters selection'
									'number' [ '@' ] reference
								'assignment'
									'expression' ['='] component 'parametrized number expression'
							)
						'text' [ 'text' ]
							'source' ['='] stategroup (
								'argument'
									'selection' component 'context command parameters selection'
									'text' [ '@' ] reference
								'property'
									'path' component 'parametrized unconstrained node selection path'
									'type' stategroup (
										'text'
											'text' [ '.' ] reference
										'id' [ '.key' ]
									)
							)
						'file' ['file']
							'source' ['='] stategroup (
								'argument'
									'selection' component 'context command parameters selection'
									'file' [ '@' ] reference
								'property'
									'path' component 'parametrized unconstrained node selection path'
									'file' [ '/' ] reference
							)
						'group' [ 'group' ]
							'update node' component 'parametrized update node'
						'reference' [ 'text' ]
							'source' ['=>'] stategroup (
								'new entry argument'
									'selection' component 'context command parameters selection'
									'reference' [ '@' 'new' ] reference
									'context node' component 'command parameter entity scoped context node selection'
								'node'
									'path' component 'parametrized unconstrained node selection path'
								'created entry' [ 'created' 'entry' ]
									'entry' stategroup (
										'ancestor' [ '.^' ]
											'context selection' component 'ancestor node selection'
										'context'
											'type' stategroup (
												'this'
												'descendant'
													'parent reference' [ '$' '>' ] reference
													'head state constraint' component 'node content constraint'
													'type' stategroup (
														'dictionary'
															'dictionary' [ '.' ] reference
														'matrix'
															'matrix' [ '%' ] reference
													)
											)
											'node constraint' component 'node content constraint'
									)
							)
						'state group' [ 'stategroup' ]
							'type' stategroup (
								'setto or update' ['=']
									'state' reference
									'node' component 'parametrized initialize node'
									'delete node' component 'delete node'
								'map' ['=' 'switch']
									'source' stategroup (
										'argument'
											'selection' ['('] component 'context command parameters selection'
											'state group parameter' [ '@' , ')' ] reference
											'mapping' [ '(' , ')' ] collection ( ['|']
												'state' [ '=' ] reference
												'node' component 'parametrized initialize node'
											)
										'property'
											'context' stategroup (
												'argument'
													'selection' [ '(' ] component 'context command parameters selection'
													'reference' [ '@' , ')' ] reference
													'path' component 'unconstrained node selection path'
													'state group' ['?'] reference
													'mapping' ['(', ')'] collection ( ['|']
														'state' [ '=' ] reference
														'initialize node' component 'parametrized initialize node'
													)
												'update'
													'path' [ '(' '$' ] component 'unconstrained node selection path'
													'state group' ['?' , ')'] reference
													'mapping' ['(', ')'] collection ( ['|']
														'state' [ '=' ] reference
														'initialize node' component 'parametrized initialize node'
													)
												'command'
													'path' ['('] component 'unconstrained node selection path'
													'state group' ['?', ')'] reference
													'mapping' ['(', ')'] collection ( ['|']
														'state' [ '=' ] reference
														'initialize node' component 'parametrized initialize node'
													)
											)
									)
									'delete node' component 'delete node'
								'update'
									'states' [ '(' , ')' ] collection indent ( ['|']
										'preceding states' collection predecessors
										'succeeding states' collection successors
										'action' stategroup (
											'setto' [ '=' ]
												'type' stategroup (
													'preceding state'
														'state' reference
													'succeeding state' [ 'forward' ]
														'state' reference
												)
												'initialize node' component 'parametrized initialize node'
											'update'
												'update node' component 'parametrized update node'
											'ignore' ['ignore']
										)
									)
							)
					)
			)
		)

### parametrized initialize node

	'parametrized initialize node' [ '(' , ')' ]
		'groups' collection indent (
			'initialize node' [ ':' 'group' ] component 'parametrized initialize node'
		)
		'texts' collection indent (
			'source' [ ':' 'text' '=' ] stategroup (
				'argument'
					'selection' component 'context command parameters selection'
					'text' [ '@' ] reference
				'property'
					'path' component 'parametrized unconstrained node selection path'
					'type' stategroup (
						'text'
							'text' [ '.' ] reference
						'id' [ '.key' ]
					)
			)
		)
		'files' collection indent (
			'source' [ ':' 'file' '=' ] stategroup (
				'argument'
					'selection' component 'context command parameters selection'
					'file' [ '@' ] reference
				'property'
					'path' component 'parametrized unconstrained node selection path'
					'file' [ '/' ] reference
			)
		)
		'matrices' collection (
			'source' [ ':' 'matrix' '=' ] stategroup (
				'empty'
				'argument'
					'type' stategroup (
						'reference'
							'selection' component 'context command parameters selection'
							'reference' [ '@' ] reference
							'context node' component 'command parameter entity scoped context node selection'
							'initialize node' component 'parametrized initialize node'
						'matrix'
							'selection' component 'context command parameters selection'
							'matrix' [ '@' '.' ] reference
							'context node' component 'command parameter entity scoped context node selection'
							'initialize node' component 'parametrized initialize node'
					)
			)
		)
		'dictionaries' collection (
			'source' [ ':' 'dictionary' '=' ] stategroup (
				'empty'
				'entry'
					'key source' stategroup (
						'argument'
							'selection' component 'context command parameters selection'
							'text' [ '@' ] reference
						'node'
							'path' component 'parametrized unconstrained node selection path'
							'dictionary' [ '.key' ] stategroup ( 'dictionary' )
					)
					'initialize node' component 'parametrized initialize node'
				'collection'
					'selection' component 'context command parameters selection'
					'matrix' [ '@' '.' ] reference
					'context node' component 'command parameter entity scoped context node selection'
					'initialize node' component 'parametrized initialize node'
			)
		)
		'numbers' collection indent (
			'set' stategroup (
				'integer' [ ':' 'integer' ]
				'natural' [ ':' 'natural' ]
			)
			'expression' [ '=' ] component 'parametrized number expression'
		)
		'references' collection indent (
			'source' [ ':' 'text' '=>' ] stategroup (
				'new entry argument'
					'selection' component 'context command parameters selection'
					'reference' [ '@' 'new' ] reference
					'context node' component 'command parameter entity scoped context node selection'
				'new entry' ['new' 'entry']
					'type' stategroup (
						'dictionary' ['.']
							'dictionary' reference
						'matrix' ['%']
							'matrix' reference
					)
					'node constraint' component 'node content constraint'
				'node'
					'path' component 'parametrized unconstrained node selection path'
				'created entry' ['created' 'entry']
					'entry' stategroup (
						'ancestor' [ '.^' ]
							'context selection' component 'ancestor node selection'
						'context'
							'type' stategroup (
								'this'
								'descendant' [ '$' ]
									'parent reference' [ '>' ] reference
									'head state constraint' component 'node content constraint'
									'type' stategroup (
										'dictionary'
											'dictionary' [ '.' ] reference
										'matrix'
											'matrix' [ '%' ] reference
									)
							)
							'node constraint' component 'node content constraint'
					)
			)
		)
		'state groups' collection indent (
			'source' [ ':' 'stategroup' '=' ] stategroup (
				'argument' ['switch']
					'selection' ['('] component 'context command parameters selection'
					'state group' [ '@' ] reference
					'KEYWORD' [')'] component 'KEYWORD'
					'states' [ '(' , ')' ] collection indent ( ['|']
						'state' [ '=' ] reference
						'initialize node' component 'parametrized initialize node'
					)
				'property' ['switch']
					'context' stategroup (
						'argument'
							'selection' ['('] component 'context command parameters selection'
							'reference' [ '@' ] reference
							'path' component 'unconstrained node selection path'
							'state group' [':'] reference
							'KEYWORD' [')'] component 'KEYWORD'
							'mapping' ['(', ')'] collection ( ['|']
								'state' ['='] reference
								'initialize node' component 'parametrized initialize node'
							)
						'update'
							'path' ['(' '$'] component 'unconstrained node selection path'
							'state group' ['?'] reference
							'KEYWORD' [')'] component 'KEYWORD'
							'mapping' ['(', ')'] collection ( ['|']
								'state' ['='] reference
								'initialize node' component 'parametrized initialize node'
							)
						'command'
							'path' ['('] component 'unconstrained node selection path'
							'state group' ['?'] reference
							'KEYWORD' [')'] component 'KEYWORD'
							'mapping' ['(', ')'] collection ( ['|']
								'state' ['='] reference
								'initialize node' component 'parametrized initialize node'
							)
					)
				'fixed'
					'state' reference
					'initialize node' component 'parametrized initialize node'
			)
		)
		// 'dictionaries' collection (
		// 	'entries' [ '->' 'dictionary' ] component 'new collection entries'
		// )
		// 'matrices' collection (
		// 	'entries' [ '->' 'matrix' ] component 'new collection entries'
		// )

### unconstrained node selection path

	'unconstrained node selection path'
		'context' stategroup (
			'this node'
				'context selection' component 'context node selection'
			'output parameter'
				'context selection' component 'context node selection'
				'type' stategroup (
					'state group output parameter'
						'state group' [ '?' ] reference
						'output parameter' [ '$' ] reference
					'referencer output'
						'referencer type' stategroup (
							'matrix' [ '>key' ]
							'output type' stategroup (
								'referenced node'
								'output parameter'
									'output parameter' [ '$' ] reference
							)
							'reference' [ '>' ]
								'reference' reference
								'output type' stategroup (
									'referenced node'
									'output parameter'
										'output parameter' [ '$' ] reference
								)
						)
				)
			'input parameter'
				'context node selection' component 'context node selection'
				'type' stategroup (
					'state' [ '&' ]
						'input parameter' reference
				)
				'tail' component 'context node selection'
		)
```
