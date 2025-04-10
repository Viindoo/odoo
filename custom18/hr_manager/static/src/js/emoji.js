/** @odoo-module **/

import { Component, useState } from '@odoo/owl';
import { registry } from '@web/core/registry';
import { standardFieldProps } from '@web/views/fields/standard_field_props';

const EMOJIS = ['😀', '😐', '😢', '😡', '😍', '😴'];

export class EmojiWidget extends Component{
	static template = 'owl.EmojiWidget';
	
	static props = {
		... standardFieldProps
	}
	
	setup(){
		const current = this.props.record.data.attitude || '';
		this.state = useState({
			selectedEmoji: current,
			showPicker: false,
			})
	}
	
	updateEmoji(emoji){
		if(!this.props.readonly){
			this.state.selectedEmoji = emoji;
			this.props.record.update({[this.props.name]: emoji})
			this.state.showPicker = false;
		}
	}
}

registry.category("fields").add("emoji", {
	component: EmojiWidget,
	supportedTypes: ["char"],
})