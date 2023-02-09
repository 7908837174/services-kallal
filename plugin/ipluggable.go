// Copyright 2023 Contributors to the Veraison project.
// SPDX-License-Identifier: Apache-2.0
package plugin

// IPluggable respresents a "pluggable" point within Veraison services. It is
// the common interfaces shared by all Veraison plugins loaded through this
// framework.
type IPluggable interface {
	// GetName returns a string containing the name of the
	// implementation of this IPluggable interface. It is the plugin name.
	GetName() string

	// GetAttestationScheme returns a string containing the name of the
	// attestation scheme handled by this IPluggable implementation.
	GetAttestationScheme() string

	// GetSupportedMediaTypes returns a []string containing the media types
	// this plugin is capable of handling.
	GetSupportedMediaTypes() []string
}
