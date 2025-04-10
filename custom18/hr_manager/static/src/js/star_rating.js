/** @odoo-module **/

import { Component, useState } from '@odoo/owl';
import { registry } from '@web/core/registry';
import { standardFieldProps } from '@web/views/fields/standard_field_props';

export class StarRatingWidget extends Component {
    static template = 'owl.StarRatingWidget';
    
    static props = {
        ...standardFieldProps,
    };

    setup() {
        const value = this.props.record.data.rating || 0;
        const cursor = this.props.readonly ? 'default' : 'pointer';
        this.state = useState({ rating: value, cursor });
    }

    updateRating(star) {
        if (!this.props.readonly) {
            this.state.rating = star;
            this.props.record.update({ [this.props.name]: star });
        }
    }
}

registry.category("fields").add("star_rating", {
  component: StarRatingWidget,
  supportedTypes: ["float"],
});
